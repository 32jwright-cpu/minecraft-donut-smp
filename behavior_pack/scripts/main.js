import { world, system } from '@minecraft/server';
import { ActionFormData } from '@minecraft/server-ui';

// ========================================
// DONUT SMP ECONOMY SYSTEM
// ========================================

const ECONOMY_CONFIG = {
  // Block selling prices
  blockPrices: {
    'dirt': 1,
    'grass_block': 2,
    'stone': 3,
    'cobblestone': 2,
    'oak_log': 5,
    'birch_log': 5,
    'spruce_log': 5,
    'dark_oak_log': 5,
    'oak_wood': 6,
    'birch_wood': 6,
    'spruce_wood': 6,
    'dark_oak_wood': 6,
    'oak_planks': 4,
    'birch_planks': 4,
    'spruce_planks': 4,
    'dark_oak_planks': 4,
    'iron_ore': 15,
    'gold_ore': 20,
    'diamond_ore': 50,
    'coal_ore': 10,
    'lapis_ore': 18,
    'redstone_ore': 12,
    'emerald_ore': 30,
    'oak_leaves': 1,
    'birch_leaves': 1,
    'spruce_leaves': 1,
    'sand': 2,
    'red_sand': 2,
    'gravel': 2,
    'clay': 3,
    'glass': 3,
    'snow': 1,
    'end_stone': 5,
    'netherrack': 2,
    'glowstone': 8
  },

  // Shop items (item name, cost)
  shopItems: {
    'iron_ingot': 20,
    'gold_ingot': 25,
    'diamond': 100,
    'emerald': 75,
    'ender_pearl': 30,
    'blaze_rod': 40,
    'netherite_ingot': 200,
    'enchanted_golden_apple': 500,
    'dragon_egg': 1000
  }
};

// Store player money
const playerMoney = new Map();
const STARTING_MONEY = 1000;

// ========================================
// MONEY MANAGEMENT FUNCTIONS
// ========================================

function getPlayerMoney(player) {
  if (!playerMoney.has(player.name)) {
    playerMoney.set(player.name, STARTING_MONEY);
  }
  return playerMoney.get(player.name);
}

function setPlayerMoney(player, amount) {
  playerMoney.set(player.name, Math.max(0, amount));
}

function addPlayerMoney(player, amount) {
  const current = getPlayerMoney(player);
  setPlayerMoney(player, current + amount);
}

// ========================================
// SELL COMMAND
// ========================================

function handleSellCommand(player) {
  const form = new ActionFormData();
  form.title('§l§6SELL BLOCKS');
  form.body('§eSelect a block to sell from your inventory:\n\n§6Blocks available in your inventory will be sold');

  const blockList = Object.entries(ECONOMY_CONFIG.blockPrices);
  blockList.forEach(([blockType, price]) => {
    form.button(`${blockType}\n§a$${price}`);
  });

  form.show(player).then((result) => {
    if (result.canceled) return;

    const selectedBlock = blockList[result.selection];
    if (!selectedBlock) return;

    const [blockType, price] = selectedBlock;
    const inventory = player.getComponent('inventory')?.container;

    if (!inventory) {
      player.sendMessage('§c❌ Error: Could not access inventory');
      return;
    }

    let found = false;
    for (let i = 0; i < inventory.size; i++) {
      const item = inventory.getItem(i);
      if (item && item.typeId === `minecraft:${blockType}`) {
        inventory.setItem(i, undefined);
        addPlayerMoney(player, price);
        player.sendMessage(`§a✓ Sold ${blockType} for §6$${price}`);
        found = true;
        break;
      }
    }

    if (!found) {
      player.sendMessage(`§c✗ You don't have any ${blockType} to sell!`);
    } else {
      const newBalance = getPlayerMoney(player);
      player.sendMessage(`§6Balance: §a$${newBalance}`);
    }
  });
}

// ========================================
// SHOP COMMAND
// ========================================

function handleShopCommand(player) {
  const form = new ActionFormData();
  form.title('§l§bSHOP');
  form.body('§eSelect an item to purchase with your money:\n\n§6Current Balance: §a$' + getPlayerMoney(player));

  const shopList = Object.entries(ECONOMY_CONFIG.shopItems);
  shopList.forEach(([itemType, cost]) => {
    form.button(`${itemType}\n§c$${cost}`);
  });

  form.show(player).then((result) => {
    if (result.canceled) return;

    const selectedItem = shopList[result.selection];
    if (!selectedItem) return;

    const [itemType, cost] = selectedItem;
    const playerBalance = getPlayerMoney(player);

    if (playerBalance < cost) {
      const needed = cost - playerBalance;
      player.sendMessage(`§c✗ Insufficient funds! You need §a$${needed}§c more.`);
      player.sendMessage(`§cCost: §6$${cost} | Your balance: §6$${playerBalance}`);
      return;
    }

    try {
      player.runCommand(`give @s minecraft:${itemType} 1`);
      addPlayerMoney(player, -cost);
      player.sendMessage(`§a✓ Purchased §6${itemType}§a for §c$${cost}`);
      player.sendMessage(`§6New Balance: §a$${getPlayerMoney(player)}`);
    } catch (error) {
      player.sendMessage('§c❌ Error: Could not purchase item!');
    }
  });
}

// ========================================
// MONEY COMMAND
// ========================================

function handleMoneyCommand(player) {
  const balance = getPlayerMoney(player);
  player.sendMessage('§l§6════════════════════════════════════');
  player.sendMessage('§l§6YOUR BALANCE');
  player.sendMessage('§l§6════════════════════════════════════');
  player.sendMessage(`§a$${balance}`);
  player.sendMessage('§6Type §b/sell §6or §b/shop §6to trade!');
  player.sendMessage('§l§6════════════════════════════════════');
}

// ========================================
// HELP COMMAND
// ========================================

function handleHelpCommand(player) {
  player.sendMessage('§l§6════════════════════════════════════');
  player.sendMessage('§l§eDONUT SMP ECONOMY COMMANDS');
  player.sendMessage('§l§6════════════════════════════════════');
  player.sendMessage('§b/sell §6- Open the sell menu');
  player.sendMessage('§b/shop §6- Open the shop menu');
  player.sendMessage('§b/money §6- Check your balance');
  player.sendMessage('§b/ehelp §6- Show this message');
  player.sendMessage('§l§6════════════════════════════════════');
}

// ========================================
// CHAT COMMAND LISTENER
// ========================================

world.beforeEvents.chatSend.subscribe((event) => {
  const { sender, message } = event;
  const command = message.trim().toLowerCase();

  if (command === '/sell') {
    event.cancel = true;
    handleSellCommand(sender);
  } else if (command === '/shop') {
    event.cancel = true;
    handleShopCommand(sender);
  } else if (command === '/money') {
    event.cancel = true;
    handleMoneyCommand(sender);
  } else if (command === '/ehelp') {
    event.cancel = true;
    handleHelpCommand(sender);
  }
});

// ========================================
// STARTUP MESSAGE
// ========================================

system.run(() => {
  console.warn('§6[ECONOMY] §aDONUT SMP ECONOMY SYSTEM LOADED!');
  console.warn('§6[ECONOMY] §eCommands: /sell, /shop, /money, /ehelp');
});
