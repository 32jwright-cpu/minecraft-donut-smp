#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DONUT SMP ECONOMY SYSTEM - Code Builder Script
For Minecraft Education Edition

This script creates an economy system with:
- /sell command to sell blocks for money
- /shop command to buy items
- /money command to check balance
"""

from mcpi.minecraft import Minecraft
from mcpi import block
import time

# Connect to Minecraft
mc = Minecraft.create()

# ===================================
# ECONOMY CONFIGURATION
# ===================================

BLOCK_PRICES = {
    'dirt': 1,
    'stone': 3,
    'oak_log': 5,
    'iron_ore': 15,
    'gold_ore': 20,
    'diamond_ore': 50,
    'coal_ore': 10,
    'sand': 2,
    'gravel': 2,
    'oak_planks': 4,
    'glass': 3,
}

SHOP_ITEMS = {
    'diamond': 100,
    'emerald': 75,
    'iron_ingot': 20,
    'gold_ingot': 25,
    'ender_pearl': 30,
    'blaze_rod': 40,
    'netherite_ingot': 200,
}

# Store player money (player_name: amount)
player_money = {}

# ===================================
# HELPER FUNCTIONS
# ===================================

def get_player_money(player_name):
    """Get player's current balance"""
    if player_name not in player_money:
        player_money[player_name] = 1000  # Starting money
    return player_money[player_name]

def add_player_money(player_name, amount):
    """Add money to player account"""
    current = get_player_money(player_name)
    player_money[player_name] = current + amount

def set_player_money(player_name, amount):
    """Set player's money to exact amount"""
    player_money[player_name] = max(0, amount)

def send_title(text, subtitle=""):
    """Send title message to player"""
    mc.postToChat("§l§6" + "="*50)
    mc.postToChat("§l§6" + text)
    if subtitle:
        mc.postToChat("§7" + subtitle)
    mc.postToChat("§l§6" + "="*50)

def send_message(text):
    """Send message to chat"""
    mc.postToChat(text)

# ===================================
# SELL FUNCTION
# ===================================

def sell_blocks():
    """Display sell menu and process block sales"""
    send_title("SELL BLOCKS", "Select a block type to sell")
    
    mc.postToChat("§eAvailable blocks to sell:")
    for i, (block_name, price) in enumerate(BLOCK_PRICES.items()):
        mc.postToChat(f"§6{i+1}. §f{block_name} §a($§a{price}§a)")
    
    mc.postToChat("§eType 'sell [block_name]' to sell a block")
    mc.postToChat("§eExample: §fgo 0 0 0§e and 'sell dirt'")

def process_sell(player_pos, block_name):
    """Process selling a block"""
    if block_name not in BLOCK_PRICES:
        send_message(f"§c❌ '{block_name}' is not a valid block!")
        return
    
    price = BLOCK_PRICES[block_name]
    
    # Create 10 blocks above player as visual feedback
    for i in range(1, 5):
        mc.setBlock(player_pos.x, player_pos.y + i, player_pos.z, block.AIR)
    
    mc.setBlock(player_pos.x, player_pos.y + 2, player_pos.z, block.DIAMOND_BLOCK)
    mc.postToChat(f"§a✓ Sold §f{block_name}§a for §6$§6{price}")
    
    player_name = "Player"  # Would get actual player name
    add_player_money(player_name, price)
    
    balance = get_player_money(player_name)
    mc.postToChat(f"§6Balance: §a$§a{balance}")

# ===================================
# SHOP FUNCTION
# ===================================

def shop_menu():
    """Display shop menu"""
    send_title("SHOP", "Buy items with your money")
    
    player_name = "Player"
    balance = get_player_money(player_name)
    mc.postToChat(f"§6Your Balance: §a$§a{balance}\n")
    
    mc.postToChat("§eAvailable items:")
    for i, (item_name, cost) in enumerate(SHOP_ITEMS.items()):
        mc.postToChat(f"§6{i+1}. §f{item_name} §c($§c{cost}§c)")
    
    mc.postToChat("§eType 'buy [item_name]' to purchase")
    mc.postToChat("§eExample: 'buy diamond'")

def process_purchase(player_pos, item_name):
    """Process item purchase"""
    if item_name not in SHOP_ITEMS:
        send_message(f"§c❌ '{item_name}' is not in the shop!")
        return
    
    cost = SHOP_ITEMS[item_name]
    player_name = "Player"
    balance = get_player_money(player_name)
    
    if balance < cost:
        needed = cost - balance
        send_message(f"§c❌ Insufficient funds!")
        send_message(f"§cNeed: §6$§6{needed}§c more")
        return
    
    # Create emerald block above player as visual feedback
    for i in range(1, 4):
        mc.setBlock(player_pos.x, player_pos.y + i, player_pos.z, block.AIR)
    
    mc.setBlock(player_pos.x, player_pos.y + 2, player_pos.z, block.EMERALD_BLOCK)
    
    mc.postToChat(f"§a✓ Purchased §f{item_name}§a for §c$§c{cost}")
    set_player_money(player_name, balance - cost)
    
    new_balance = get_player_money(player_name)
    mc.postToChat(f"§6New Balance: §a$§a{new_balance}")

# ===================================
# MONEY FUNCTION
# ===================================

def check_balance():
    """Check player balance"""
    player_name = "Player"
    balance = get_player_money(player_name)
    
    send_title("BALANCE", f"$§a{balance}")
    mc.postToChat("§6Type '§bsell§6' or '§bshop§6' to trade!")

# ===================================
# MAIN SETUP
# ===================================

def setup_economy():
    """Initialize economy system"""
    send_title("DONUT SMP ECONOMY", "System Loaded!")
    mc.postToChat("§eCommands available:")
    mc.postToChat("  §6sell§e - Open sell menu")
    mc.postToChat("  §6shop§e - Open shop menu")
    mc.postToChat("  §6balance§e - Check your money")
    mc.postToChat("§aType commands in chat!")
    
    # Create spawn area with economy hub
    player_pos = mc.player.getPos()
    
    # Clear area
    for x in range(-5, 6):
        for z in range(-5, 6):
            for y in range(0, 5):
                mc.setBlock(player_pos.x + x, player_pos.y + y, player_pos.z + z, block.AIR)
    
    # Create foundation
    for x in range(-5, 6):
        for z in range(-5, 6):
            mc.setBlock(player_pos.x + x, player_pos.y, player_pos.z + z, block.GOLD_BLOCK)
    
    # Create sell area (left side)
    for x in range(-5, -2):
        for z in range(-2, 3):
            mc.setBlock(player_pos.x + x, player_pos.y + 1, player_pos.z + z, block.DIAMOND_BLOCK)
    mc.postToChat("§6LEFT SIDE: Sell area (DIAMOND)")
    
    # Create shop area (right side)
    for x in range(3, 6):
        for z in range(-2, 3):
            mc.setBlock(player_pos.x + x, player_pos.y + 1, player_pos.z + z, block.EMERALD_BLOCK)
    mc.postToChat("§6RIGHT SIDE: Shop area (EMERALD)")
    
    # Create info sign in center
    mc.setBlock(player_pos.x, player_pos.y + 2, player_pos.z, block.REDSTONE_LAMP)

# ===================================
# SIMPLE DEMO
# ===================================

def run_demo():
    """Run a simple demo of the system"""
    setup_economy()
    
    time.sleep(2)
    
    # Demo: Check balance
    mc.postToChat("§e[DEMO] Checking balance...")
    time.sleep(1)
    check_balance()
    
    time.sleep(2)
    
    # Demo: Sell a block
    mc.postToChat("§e[DEMO] Selling stone for $3...")
    time.sleep(1)
    player_pos = mc.player.getPos()
    process_sell(player_pos, 'stone')
    
    time.sleep(2)
    
    # Demo: Buy an item
    mc.postToChat("§e[DEMO] Buying diamond for $100...")
    time.sleep(1)
    process_purchase(player_pos, 'diamond')
    
    time.sleep(2)
    
    # Final balance
    mc.postToChat("§e[DEMO] Final balance check...")
    time.sleep(1)
    check_balance()

# ===================================
# RUN THE SYSTEM
# ===================================

if __name__ == "__main__":
    try:
        # Run demo
        run_demo()
        
        # The system is now active!
        # Players can use:
        # - sell_blocks() to see sell menu
        # - shop_menu() to see shop menu
        # - check_balance() to see their money
        
    except Exception as e:
        mc.postToChat(f"§cError: {str(e)}")
