# TTM Chatroom

## About

Welcome to TTM Chatroom, an open-source, secure chat application with a sleek twilight-themed GUI. TTM stands for Tri-Tiered Messaging, its functionality and features are cutting-edge, designed to provide a seamless and secure chatting experience.

## Key Features

- **Base64 End-to-End Encryption**: Ensures that all messages are securely encrypted, protecting your conversations from prying eyes.
- **Robust Logging**: Comprehensive logging system that keeps track of all activities for security and troubleshooting purposes.
- **Twilight Theme**: A modern and visually appealing theme for the client interface, providing a pleasant user experience.
- **Account Management**: Uses an `accounts.json` file on the server to control who can join the chatroom, ensuring only authorized users have access.
- **Open Source**: Fully open-source project, allowing you to inspect, modify, and contribute to the codebase.

## Architecture

TTM Chatroom employs a unique architecture to manage client connections and distribute loads efficiently:

```
Server <-----> Distributors <-----> Clients
```

### Components

- **Server**: 
  - Manages authentication and main logs

  - Stores user account information in `accounts.json`
  - Does not directly interact with clients but communicates with distributors

- **Distributors**:
  - Handle client connections
  - Distribute the load among multiple clients
  - Act as intermediaries between clients and the server
  - Collect logs and send them to the server upon shutdown

- **Clients**:
  - Communicate with distributors for all operations
  - Utilize a twilight-themed GUI for an enhanced user experience
  - Perform login authentication via the distributor

## Getting Started

### Prerequisites

- Python 3.x
- Necessary Python libraries (listed in `requirements.txt`)

### Running the Chatroom

1. **Start the server**:
   ```sh
   python server.py
   ```

2. **Start the distributor(s)**:
   ```sh
   python distributor.py
   ```

3. **Run the client(s)**:
   ```sh
   python client.py
   ```

## Contributing

We welcome contributions from the community! Please fork the repository and submit pull requests for any features, bug fixes, or improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact

Created by Janco.

---

Thank you for using TTM Chatroom! Enjoy secure and seamless communication with our cutting-edge chat application.
