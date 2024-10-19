# Splitter
![Slpitter](https://drive.google.com/uc?export=view&id=1IaKWsVTCrbXyFvnL2QgjzdUsOQfNvIDC)
This project is a Discord bot developed using Python that helps manage voice channels in a Discord server. It allows users to create, manage, and reset voice channels based on specified topics and user participation.

## Features

- Create a new server document in MongoDB.
- Change topics for voice channels.
- Reset topics for voice channels.
- Show current topics.
- Change User Participation Ratio (UPR).
- Delete server documents from MongoDB.
- Split users from a voice channel into smaller groups based on UPR.

## Commands

- `!sp create_server`: Create a new server document.
- `!sp change_topics <topics>`: Change the topics for voice channels.
- `!sp reset_topics`: Reset the topics to default.
- `!sp topics`: Show the current topics.
- `!sp change_upr <UPR>`: Change the User Participation Ratio.
- `!sp delete_server`: Delete the server document from MongoDB.
- `!sp split`: Split users in a voice channel into groups based on UPR.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/FelipPalermo/splitter.git
   ```
2. Navigate to the project directory:
   ```bash
   cd splitter
   ```
3. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
4. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
5. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
6. Set up your Discord bot token and MongoDB connection string in environment variables.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

