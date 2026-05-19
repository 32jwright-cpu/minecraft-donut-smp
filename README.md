# Minecraft Donut SMP Economy System

A Minecraft Education Edition script that adds a selling system and shop system inspired by the famous Donut SMP.

## 🎮 Features

- **`/sell`** - Opens a menu to sell blocks for money
- **`/shop`** - Opens a menu to buy items with money
- **`/money`** - Check your current balance
- Progressive block values (common blocks worth less, rare blocks worth more)
- Player money tracking with starting balance of $1000
- Easy to customize prices and items

## 📦 Installation

1. Download this repository
2. Copy the `behavior_pack` folder into your Minecraft world's behavior packs
3. Enable the behavior pack in world settings
4. Join the world and start using commands!

## 🛠️ Commands

### `/sell` - Sell Blocks for Money
- Opens a menu with all available blocks you can sell
- Select a block and it will be removed from your inventory
- You'll receive money instantly
- Block prices range from $1 (dirt) to $50 (diamond ore)

### `/shop` - Buy Items with Money
- Opens a menu with premium items for purchase
- Select an item and spend your money
- Item will be added to your inventory
- Prices range from $20 (iron ingot) to $1000 (dragon egg)

### `/money` - Check Balance
- Shows your current money balance
- Everyone starts with $1000

## 💰 Block Prices (Selling)

| Block | Price |
|-------|-------|
| Dirt, Grass | $1-2 |
| Stone, Cobblestone | $2-3 |
| Logs, Wood | $5-6 |
| Planks | $4 |
| Iron Ore | $15 |
| Coal Ore | $10 |
| Gold Ore | $20 |
| Lapis Ore | $18 |
| Redstone Ore | $12 |
| Emerald Ore | $30 |
| Diamond Ore | $50 |

## 🛍️ Shop Items (Buying)

| Item | Price |
|------|-------|
| Iron Ingot | $20 |
| Gold Ingot | $25 |
| Diamond | $100 |
| Emerald | $75 |
| Ender Pearl | $30 |
| Blaze Rod | $40 |
| Enchanted Golden Apple | $500 |
| Netherite Ingot | $200 |
| Dragon Egg | $1000 |

## 🎯 How to Use

1. **Gather Resources**: Mine blocks to collect items
2. **Sell Items**: Type `/sell` and select blocks to sell
3. **Earn Money**: Get paid for selling blocks
4. **Buy Premium Items**: Type `/shop` to purchase rare items with your earnings
5. **Check Balance**: Use `/money` to see how much you have

## 📝 File Structure

```
minecraft-donut-smp/
├── README.md                    # This file
├── behavior_pack/
│   ├── pack_manifest.json       # Pack configuration
│   └── scripts/
│       └── main.js              # Main economy system code
└── .gitignore                   # Git ignore file
```

## 🔧 Customization

To customize prices and items, edit `behavior_pack/scripts/main.js`:

```javascript
const ECONOMY_CONFIG = {
  blockPrices: {
    'dirt': 1,
    'diamond_ore': 50,
    // Add more blocks here
  },
  shopItems: {
    'diamond': 100,
    'dragon_egg': 1000,
    // Add more items here
  }
};
```

## 📖 Requirements

- Minecraft Education Edition or Bedrock Edition
- Support for scripting API
- Behavior pack enabled in world settings

## 🚀 Getting Started

1. Download the files
2. Add behavior pack to your world
3. Enable the pack in settings
4. Type `/sell`, `/shop`, or `/money` in chat
5. Enjoy your economy system!

## 💡 Tips

- Start by mining common blocks to build up initial capital
- Sell higher-value ores to earn more money faster
- Save up for rare items in the shop
- Work with friends to create trading opportunities!

## 📄 License

Free to use and modify for your Minecraft servers and worlds!

Have fun building your Donut SMP economy! 🍩
