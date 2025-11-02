import { Connection, PublicKey } from '@solana/web3.js';
import WebSocket from 'ws';
import express from 'express';
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Express app
const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server });

// Serve static files from public directory
app.use(express.static(join(__dirname, 'public')));

// Solana RPC endpoint
const SOLANA_WS_ENDPOINT = 'wss://api.mainnet-beta.solana.com';
const HTTP_ENDPOINT = 'https://api.mainnet-beta.solana.com';

// Store for tracking mints
const trackedMints = new Map();
const CONFIRMED_MINTS = new Set();
const MINT_LENGTH = 44;
const MAX_AGE_SECONDS = 0.5;

// Log buffer for web clients (last 100 log entries)
const logBuffer = [];
const MAX_LOG_BUFFER = 100;

// WebSocket clients
const clients = new Set();

// API endpoint to get mints
app.get('/api/mints', (req, res) => {
  const mints = Array.from(trackedMints.values());
  res.json(mints);
});

// API endpoint to get logs
app.get('/api/logs', (req, res) => {
  res.json(logBuffer);
});

// Add log to buffer and broadcast
function addLog(message, type = 'info') {
  const logEntry = {
    timestamp: new Date().toISOString(),
    message,
    type
  };

  logBuffer.push(logEntry);

  // Keep buffer size limited
  if (logBuffer.length > MAX_LOG_BUFFER) {
    logBuffer.shift();
  }

  // Broadcast to all clients
  broadcast({ type: 'log', data: logEntry });
}

// Broadcast message to all clients
function broadcast(data) {
  const message = JSON.stringify(data);
  clients.forEach(client => {
    if (client.readyState === client.OPEN) {
      client.send(message);
    }
  });
}

// Send new mint to all clients
function broadcastMint(mintData) {
  broadcast({ type: 'new_mint', data: mintData });
}

/**
 * Check if a string is a valid Solana address (base58, 44 chars)
 */
function isValidSolanaAddress(str) {
  if (str.length !== MINT_LENGTH) return false;
  try {
    new PublicKey(str);
    return true;
  } catch {
    return false;
  }
}

/**
 * Extract potential mint addresses from logs
 */
function extractMintAddresses(logs) {
  const addresses = new Set();
  
  if (!logs || !Array.isArray(logs)) return addresses;
  
  for (const log of logs) {
    if (typeof log === 'string') {
      const words = log.split(/\s+/);
      for (const word of words) {
        if (word.length === MINT_LENGTH && isValidSolanaAddress(word)) {
          addresses.add(word);
        }
      }
    }
  }
  
  return addresses;
}

/**
 * Check mint age using RPC call
 */
async function checkMintAge(connection, mintAddress, currentTime, transactionSignature) {
  try {
    const mintPubkey = new PublicKey(mintAddress);
    const sigs = await connection.getSignaturesForAddress(mintPubkey, { limit: 1 });
    
    if (sigs && sigs.length > 0) {
      const blockTime = sigs[0].blockTime;
      if (blockTime) {
        const ageSeconds = currentTime - blockTime;
        const isFresh = ageSeconds <= MAX_AGE_SECONDS;
        
        if (isFresh) {
          addLog(`✅ Fresh mint found: ${mintAddress} (age: ${ageSeconds.toFixed(3)}s)`, 'success');
        } else {
          addLog(`⏭️ Skipping old mint: ${mintAddress} (age: ${ageSeconds.toFixed(3)}s)`, 'skip');
        }
        
        return isFresh;
      }
    }
    
    return false;
  } catch (error) {
    addLog(`❌ Error checking mint age for ${mintAddress}: ${error.message}`, 'error');
    return false;
  }
}

/**
 * Process a mint address
 */
async function processMint(connection, mintAddress, currentTime, transactionSignature) {
  if (CONFIRMED_MINTS.has(mintAddress)) {
    addLog(`⏭️ Already processed: ${mintAddress}`, 'skip');
    return;
  }

  addLog(`🔍 Checking mint: ${mintAddress}`, 'search');

  try {
    const isFresh = await checkMintAge(connection, mintAddress, currentTime, transactionSignature);
    
    if (isFresh) {
      CONFIRMED_MINTS.add(mintAddress);
      
      const mintData = {
        mint: mintAddress,
        transaction: transactionSignature,
        foundAt: new Date().toISOString(),
        timestamp: currentTime
      };
      
      trackedMints.set(mintAddress, mintData);
      
      // Broadcast to web clients
      broadcastMint(mintData);
      
      // Also log to console
      console.log(`✨ NEW FRESH MINT: ${mintAddress}`);
      console.log(`   Transaction: ${transactionSignature}`);
      console.log(`   Time: ${mintData.foundAt}`);
    }
  } catch (error) {
    addLog(`❌ Error processing mint ${mintAddress}: ${error.message}`, 'error');
  }
}

/**
 * Main WebSocket connection handler
 */
async function connectToSolana() {
  addLog('🚀 Connecting to Solana WebSocket...', 'process');
  
  const connection = new Connection(HTTP_ENDPOINT, 'confirmed');
  const ws = new WebSocket(SOLANA_WS_ENDPOINT);
  
  ws.on('open', () => {
    addLog('✅ Connected to Solana WebSocket', 'success');
    
    const subscribeMessage = {
      jsonrpc: "2.0",
      id: 1,
      method: "logsSubscribe",
      params: [
        {
          mentions: ["TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"]
        },
        {
          commitment: "confirmed"
        }
      ]
    };
    
    ws.send(JSON.stringify(subscribeMessage));
  });
  
  ws.on('message', async (data) => {
    try {
      const response = JSON.parse(data.toString());
      
      if (response.method === 'logsNotification' && response.params) {
        const logs = response.params.result;
        const signature = logs.value.signature;
        
        addLog(`📝 Processing transaction: ${signature.substring(0, 16)}...`, 'process');
        
        const addresses = extractMintAddresses(logs.value.logs);
        
        if (addresses.size > 0) {
          addLog(`🔍 Found ${addresses.size} potential mint(s) in transaction ${signature}`, 'search');
          
          const currentTime = Math.floor(Date.now() / 1000);
          
          // Process each address
          for (const address of addresses) {
            await processMint(connection, address, currentTime, signature);
          }
        }
      }
    } catch (error) {
      addLog(`❌ Error processing message: ${error.message}`, 'error');
    }
  });
  
  ws.on('error', (error) => {
    addLog(`❌ WebSocket error: ${error.message}`, 'error');
  });
  
  ws.on('close', () => {
    addLog('⚠️ WebSocket disconnected. Reconnecting...', 'warning');
    setTimeout(() => connectToSolana(), 5000);
  });
}

// WebSocket server for web clients
wss.on('connection', (ws) => {
  clients.add(ws);
  addLog(`📱 New client connected. Total: ${clients.size}`, 'info');

  // Send all existing mints to the new client
  const mints = Array.from(trackedMints.values());
  ws.send(JSON.stringify({ type: 'all_mints', data: mints }));

  // Send all existing logs to the new client
  ws.send(JSON.stringify({ type: 'all_logs', data: logBuffer }));

  ws.on('close', () => {
    clients.delete(ws);
    addLog(`📱 Client disconnected. Total: ${clients.size}`, 'info');
  });
});

// Start server
const PORT = 3000;
server.listen(PORT, () => {
  console.log(`🌐 Server running at http://localhost:${PORT}`);
  addLog(`🌐 Server running at http://localhost:${PORT}`, 'success');
  connectToSolana();
});










