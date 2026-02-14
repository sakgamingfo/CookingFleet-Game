import json
import os
import random

SLOTS = ['slot1.json', 'slot2.json', 'slot3.json']

# ================= ACCOUNT SYSTEM =================
def create_account(slot_file):
    username = input("👤 Create username: ").strip()
    password = input("🔒 Create password: ").strip()
    
    data = {
        "username": username,
        "password": password,
        "money": 50,
        "inventory": {},
        "dishes": {},
        "recipes": ['🍪 cookie'],
        "unlock_level": 0,
        "total_cooked": 0
    }
    
    with open(slot_file, 'w') as f:
        json.dump(data, f, indent=4)
    print("✅ Account created!")
    return data


def load_account(slot_file):
    if not os.path.exists(slot_file):
        print("❌ Slot empty!")
        return None

    with open(slot_file, 'r') as f:
        data = json.load(f)

    username = input("👤 Username: ").strip()
    password = input("🔒 Password: ").strip()

    if username == data["username"] and password == data["password"]:
        print("🔓 Login successful!")
        return data
    else:
        print("❌ Wrong login!")
        return None


def delete_account(slot_file):
    if os.path.exists(slot_file):
        os.remove(slot_file)
        print("🗑️ Account deleted!")
    else:
        print("Slot already empty.")

# ================= GAME FUNCTIONS =================

SHOP_ITEMS = {
    '🌾 flour': 2,
    '🍬 sugar': 3,
    '🥚 eggs': 4,
    '🥛 milk': 5,
    '🍫 chocolate': 6
}

RECIPES = {
    '🍪 cookie': {
        'ingredients': {'🌾 flour': 1, '🍬 sugar': 1},
        'sell_price': 8,
        'fun_message': "🍪 Crunchy cookie! Customer: 'Nom nom, best ever!'"
    },
    '🎂 cake': {
        'ingredients': {'🌾 flour': 2, '🍬 sugar': 2, '🥚 eggs': 2, '🥛 milk': 1},
        'sell_price': 25,
        'fun_message': "🎂 Fluffy cake explosion of joy!"
    },
    '🍫 brownie': {
        'ingredients': {'🌾 flour': 1, '🍬 sugar': 1, '🍫 chocolate': 2, '🥚 eggs': 1},
        'sell_price': 18,
        'fun_message': "🍫 Gooey brownie magic!"
    }
}

FUN_EVENTS = [
    "✨ Your dish glows with magic! Double profit!",
    "💵 Customer tips extra!",
    "🐱 Pet cat adds flavor!",
    "🎆 Mini firework show!",
    "⭐ Perfect bake!"
]


def save_game(data, slot_file):
    with open(slot_file, 'w') as f:
        json.dump(data, f, indent=4)
    print("💾 Game saved!")


def print_status(data):
    print(f"\n💰 Money: ${data['money']}")
    print("📦 Inventory:", data['inventory'])
    print("🍳 Dishes:", data['dishes'])
    print("📈 Cooked:", data['total_cooked'])


def check_unlocks(data):
    if data['total_cooked'] >= 5 and '🎂 cake' not in data['recipes']:
        data['recipes'].append('🎂 cake')
        print("🎉 Cake unlocked!")
    if data['total_cooked'] >= 15 and '🍫 brownie' not in data['recipes']:
        data['recipes'].append('🍫 brownie')
        print("🚀 Brownie unlocked!")


def shop(data):
    print("\n🛒 === SHOP === 🛒")
    for item, price in SHOP_ITEMS.items():
        print(f"  {item}: ${price}")

    choice = input("💳 Buy what? (or 'q' to quit): ").lower()
    if choice in SHOP_ITEMS and data['money'] >= SHOP_ITEMS[choice]:
        data['money'] -= SHOP_ITEMS[choice]
        data['inventory'][choice] = data['inventory'].get(choice, 0) + 1
        print(f"✅ Bought {choice}!")
    elif choice != 'q':
        print("❌ Can't buy that.")


def cook(data):
    print("\n👨‍🍳 === RECIPES === 👨‍🍳")
    for r in data['recipes']:
        print(f"  🔹 {r}")

    choice = input("🍳 Cook what? (or 'q' to quit): ").lower()
    if choice == 'q':
        return

    if choice not in data['recipes']:
        print("❌ Not unlocked!")
        return

    recipe = RECIPES[choice]

    for ing, amt in recipe['ingredients'].items():
        if data['inventory'].get(ing, 0) < amt:
            print(f"❌ Missing ingredients! Need {amt}x {ing}")
            return

    for ing, amt in recipe['ingredients'].items():
        data['inventory'][ing] -= amt

    print(random.choice(FUN_EVENTS))

    data['dishes'][choice] = data['dishes'].get(choice, 0) + 1
    data['total_cooked'] += 1
    check_unlocks(data)
    print("✅", recipe['fun_message'])


def sell(data):
    if not data['dishes']:
        print("❌ No dishes to sell.")
        return

    print("\n💵 === SELL DISHES === 💵")
    for dish, count in data['dishes'].items():
        price = RECIPES[dish]['sell_price']
        print(f"  📦 {dish}: {count} available @ ${price} each")

    choice = input("💰 Sell what? (or 'q' to quit): ").lower()
    if choice == 'q':
        return

    if choice in data['dishes'] and data['dishes'][choice] > 0:
        data['dishes'][choice] -= 1
        profit = RECIPES[choice]['sell_price']
        data['money'] += profit
        print(f"✅ Sold {choice} for ${profit}! 🤑")
    else:
        print("❌ Can't sell that.")


# ================= MAIN GAME LOOP =================

print("🍳 Welcome to CookingFleet! The ULTIMATE fun cooking game! 🚀")
print("Type 'start' to begin your chef adventure!")

while True:
    start_input = input("> ").strip().lower()
    if start_input == 'start':
        break
    print("👆 Type 'start' exactly to play!")

print("\n📁 === SAVE SLOTS === 📁")
for i, slot in enumerate(SLOTS):
    status = "🟢 Empty"
    if os.path.exists(slot):
        status = "🔴 Taken"
    print(f"  {i+1}. 💾 Slot {i+1} ({status})")

try:
    slot_choice = int(input("🎯 Choose slot (1-3): ")) - 1
    slot_file = SLOTS[slot_choice]
except:
    print("❌ Invalid slot.")
    exit()

print("""
╔═══════════════════════════╗
║   🎮 ACCOUNT MENU 🎮      ║
╠═══════════════════════════╣
║  1. ➕ Create Account     ║
║  2. 🔓 Load Account       ║
║  3. 🗑️  Delete Account     ║
╚═══════════════════════════╝
""")

action = input("🎯 Choose option: ")

if action == '1':
    data = create_account(slot_file)
elif action == '2':
    data = load_account(slot_file)
    if not data:
        exit()
elif action == '3':
    delete_account(slot_file)
    exit()
else:
    print("❌ Invalid option.")
    exit()

print(f"\n🎉 Welcome to CookingFleet, {data['username']}! 🎉")
print(f"💰 You have ${data['money']}.")

while True:
    print("""
    ╔════════════════════════════╗
    ║     🍳 COOKING FLEET 🍳    ║
    ╠════════════════════════════╣
    ║  1. 📊 View Stats          ║
    ║  2. 🛒 Shop                ║
    ║  3. 👨‍🍳 Cook                ║
    ║  4. 💵 Sell                ║
    ║  5. 💾 Save & Exit         ║
    ╚════════════════════════════╝
    """)

    choice = input("🎮 Choose: ")

    if choice == "1":
        print_status(data)

    elif choice == "2":
        shop(data)

    elif choice == "3":
        cook(data)

    elif choice == "4":
        sell(data)

    elif choice == "5":
        save_game(data, slot_file)
        print("👋 Goodbye!")
        break

    else:
        print("❌ Invalid option.")
