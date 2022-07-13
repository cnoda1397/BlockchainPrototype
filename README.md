# BlockchainPrototype
 Basic Blockchain Web app based on GeeksForGeeks tutorial

Instructions:
1. install requirements
2. Open Terminal
 3. Enter export FLASK_APP=bloackchain
 4. Enter export FLASK_ENV=development
 5. Enter flask run
6. Follow the link in the terminal to localhost 
7. Append any of the following to the url:
 - /get_chain => print the entire blockchain
 - /mine_block => add a block with a random payload to the chain
 - /custom_block/<Your Payload Here> => add a block with a custom payload of digits
 - /valid => checks if the blockchain is valid