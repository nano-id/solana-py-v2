import { Connection, PublicKey } from '@solana/web3.js';
import WebSocket from 'ws';

// Solana RPC endpoint (you can replace with your own)
const SOLANA_WS_ENDPOINT = 'wss://api.mainnet-beta.solana.com';
const HTTP_ENDPOINT = 'https://api.mainnet-beta.solana.com';

// Database to store mint addresses and their timestamps
const trackedMints = new Map();
const CONFIRMED_MINTS = new Set();

// Configuration
const MINT_LENGTH = 44; // Solana address length
const MAX_AGE_SECONDS = 0.6; // Only track mints created within 0.6 seconds

/**
 * Check if a string is a valid Solana address (base58, 44 chars)
 */
function isValidSolanaAddress(str) {
  if (str.length !== MINT_LENGTH) return false;
  try {
    // Try to create a PublicKey to validate
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
      // Split by whitespace and filter for 44-char addresses
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
async function checkMintAge(connection, mintAddress, currentTime) {
  try {
    const mintPubkey = new PublicKey(mintAddress);
    const accountInfo = await connection.getAccountInfo(mintPubkey);
    
    if (accountInfo) {
      // Account exists - calculate age
      const accountAge = currentTime - (accountInfo.lamports / 1000000); // Approximate
      
      // Try to get transaction signatures to determine actual creation time
      const sigs = await connection.getSignaturesForAddress(mintPubkey, { limit: 1 });
      
      if (sigs && sigs.length > 0) {
        const blockTime = sigs[0].blockTime;
        if (blockTime) {
          const ageSeconds = currentTime - blockTime;
          return ageSeconds <= MAX_AGE_SECONDS;
        }
      }
      
      // Fallback: assume new if we can't determine age
      return false;
    }
    
    return false;
  } catch (error) {
    console.error(`Error checking mint age for ${mintAddress}:`, error.message);
    return false;
  }
}

/**
 * Main WebSocket connection handler
 */
async function connectToSolana() {
  console.log('🚀 Connecting to Solana WebSocket...');
  
  const connection = new Connection(HTTP_ENDPOINT, 'confirmed');
  const ws = new WebSocket(SOLANA_WS_ENDPOINT);
  
  ws.on('open', () => {
    console.log('✅ Connected to Solana WebSocket');
    
    // Subscribe to logs from program (SplToken program for token mints)
    // You may need to adjust the program ID based on what you're tracking
    const subscription = {
      jsonrpc: '2.0',
      id: 1,
      method: 'logsSubscribe',
      params: [
        {
          mentions: ['TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA'] // SPL Token Program
        },
        {
          commitment: 'confirmed'
        }
      ]
    };
    
    ws.send(JSON.stringify(subscription));
  });
  
  ws.on('message', async (data) => {
    try {
      const message = JSON.parse(data.toString());
      
      if (message.method === 'logsNotification') {
        const logs = message.params?.result?.value?.logs || [];
        const signature = message.params?.result?.value?.signature;
        const slot = message.params?.result?.value?.slot;
        
        // Extract mint addresses from logs
        const mintAddresses = extractMintAddresses(logs);
        
        if (mintAddresses.size > 0) {
          console.log(`\n🔍 Found ${mintAddresses.size} potential mint(s) in transaction ${signature}`);
          
          const currentTime = Date.now() / 1000;
          
          for (const mintAddress of mintAddresses) {
            if (!CONFIRMED_MINTS.has(mintAddress)) {
              // Check if this mint is fresh (created within 0.6 seconds)
              const isFresh = await checkMintAge(connection, mintAddress, currentTime);
              
              if (isFresh || !trackedMints.has(mintAddress)) {
                trackedMints.set(mintAddress, {
                  address: mintAddress,
                  transaction: signature,
                  timestamp: new Date().toISOString(),
                  slot: slot
                });
                
                console.log(`✨ NEW FRESH MINT: ${mintAddress}`);
                console.log(`   Transaction: ${signature}`);
                console.log(`   Time: ${new Date().toISOString()}`);
                
                // Add to confirmed set to avoid reprocessing
                CONFIRMED_MINTS.add(mintAddress);
                
                // Save to file or process further
                await saveMint(mintAddress, signature);
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('❌ Error processing message:', error.message);
    }
  });
  
  ws.on('error', (error) => {
    console.error('❌ WebSocket error:', error.message);
  });
  
  ws.on('close', () => {
    console.log('⚠️ WebSocket closed. Reconnecting in 5 seconds...');
    setTimeout(connectToSolana, 5000);
  });
  
  // Handle ping/pong to keep connection alive
  setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.ping();
    }
  }, 30000);
}

/**
 * Save mint address to file
 */
async function saveMint(mintAddress, signature) {
  try {
    const fs = await import('fs/promises');
    const content = `${new Date().toISOString()},${mintAddress},${signature}\n`;
    await fs.appendFile('mint_addresses.csv', content);
  } catch (error) {
    // If file write fails, just log it
    console.error('Could not save to file:', error.message);
  }
}

// Initialize
console.log('🎯 Solana Meme Coin Mint Tracker');
console.log(`📋 Tracking mint addresses created within ${MAX_AGE_SECONDS} seconds\n`);

connectToSolana();

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n\n👋 Shutting down gracefully...');
  console.log(`📊 Total unique mints tracked: ${trackedMints.size}`);
  process.exit(0);
});


