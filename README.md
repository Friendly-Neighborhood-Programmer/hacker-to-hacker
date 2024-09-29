# Hacker-to-Hacker
Welcome to the Hacker Network, a place where all your file transfer dreams can come true.

# Run Instructions
```
pip install -r ./requirements.txt
```
From within the source directory run
```
python client.py
```
Follow the instructions on screen

## Inspiration: 
With the rise of decentralized technologies, we wanted to explore the foundations of peer-to-peer (P2P) networks. We set out to build a fully functioning P2P network from scratch using Python. Our goal was to create a basic yet robust system that could handle the decentralized exchange of data between peers, without relying on a central server.

## What It Does: 
HTH enables direct communication between multiple nodes (peers) in the network. Peers can share messages and files without the need for a central authority. 

## Key Features
Peer Discovery: Nodes can discover and connect to other active peers in the network.

Data Transmission: The system supports the transfer of serialized data (using Python’s pickle module), including files, messages, or any object.

Decentralized Architecture: There is no need for a central server, enabling a truly distributed network.

Tracker: Available files can be found by pinging the tracker, showing which files can be downloaded and from which users.

How We Built It: We built HTH using Python and its socket library to manage peer-to-peer communication. The core functionality was established by implementing a socket-based system where each peer could act as both a client and a server. For serialization, we utilized the pickle library, which allowed us to efficiently serialize and deserialize Python objects for transmission between peers.


## Key Components
Sockets: Managed network connections and data exchange between peers.

Pickle: Serialized and deserialized Python objects for transmission.

Threading: Handled concurrent connections and allowed peers to send and receive data simultaneously.

Dynamic Peer Management: Developed logic for handling peer connections, ensuring the network remained intact as peers joined or left.

##Challenges We Ran Into:
Synchronization Issues: Ensuring all peers remained synchronized when one or more peers joined or left the network was tricky. We had to carefully manage peer discovery and reconnections.

Data Integrity: Preserving the integrity of the data being transferred between peers required implementing safeguards against data loss or corruption.

Thread Management: Handling multiple concurrent connections efficiently required deep control over Python's threading to avoid bottlenecks and race conditions.

## What We Learned: 
Building a P2P network from scratch taught us a lot about network protocols, socket programming, and the importance of thread management in concurrent systems. We also gained a deeper understanding of the challenges involved in decentralized systems, such as maintaining consistent communication and ensuring data integrity across all nodes.

## Accomplishments that we're proud of
We are proud that our P2P network can transfer files at fast speeds while distributing the stress of uploading across the system. We're also proud that we created our network with minimal pre-existing code and libraries.

## What’s Next
Encryption: To ensure secure data transmission between peers.

Peer Reputation System: To detect and manage malicious or faulty peers.

Improved User Interface: To make it easier for users to interact with the network.

File Sharing Improvements: Optimizing file transfer mechanisms for larger files and faster throughput.

