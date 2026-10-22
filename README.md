# 🛡️ Marzban Store & Provisioning Bot

A Telegram-based automated storefront and provisioning system integrated with the **Marzban Panel**. This bot allows users to request VPN configurations with specific bandwidth and duration limits, leveraging a secure admin-approval workflow before final delivery.

This project demonstrates practical experience with Third-Party API integrations, order management, and secure administrative workflows.

## ✨ Key Features

### 🔌 Marzban API Integration
* **Dynamic Provisioning:** Automatically communicates with the Marzban API to generate VPN profiles.
* **Custom Limits:** Passes specific bandwidth (GB) and time/duration parameters directly to the panel based on the user's order.
* **Instant Delivery:** Fetches the generated config from Marzban and delivers it directly to the user's Telegram chat upon approval.

### 🛂 Admin Approval Workflow
* **Order Queue System:** User requests are not processed immediately; they are placed in a pending state and sent to the admin.
* **One-Click Moderation:** Admins receive detailed order summaries via an inline keyboard to instantly **Approve** or **Reject** requests.
* **Secure Delivery:** The integration with Marzban is only triggered *after* admin verification, preventing abuse or unauthorized generation.

### 🛒 E-Commerce & Store Logic
* **User Dashboard:** Users can track the status of their pending, approved, or rejected orders.
* **Flexible Packages:** Easily configurable plans for different data volumes and expiration timelines.

## 🛠️ Tech Stack & Architecture

* **Language:** Python 3.x
* **Bot Framework:** pyTelegramBotAPI / python-telegram-bot
* **External Services:** Marzban Panel REST API
* **Database:** (e.g., PostgreSQL / SQLite) for tracking order statuses and user IDs.
* **Authentication:** Token-based API authentication for Marzban.

## 🚀 Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mohammadmahdiahmadipour4-glitch/vpn-store-bot.git
   cd vpn-store-bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration:**
   Create a `.env` file based on `.env.example` and add your credentials:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   ADMIN_CHAT_ID=your_telegram_id
   MARZBAN_API_URL=https://your-marzban-domain.com/api
   MARZBAN_USERNAME=admin
   MARZBAN_PASSWORD=secure_password
   ```

4. **Run the bot:**
   ```bash
   python main.py
   ```

## 🔄 How It Works (The Workflow)

1. **User Request:** The user selects a package (e.g., 50GB, 1 Month) and submits a request.
2. **Admin Notification:** The bot forwards the request details to the Admin's Telegram chat.
3. **Approval:** If the admin clicks "Approve", the bot authenticates with the Marzban API, sends a POST request with the specific bandwidth and expiration parameters, and retrieves the generated link.
4. **Fulfillment:** The bot sends the final configuration link to the user.