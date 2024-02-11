// SPDX-License-Identifier: MIT
pragma solidity ^0.6.4;

contract Owned {
    address payable public owner;

    constructor() public {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner, "Only the contract owner can call this function");
        _;
    }
}

abstract contract Mortal is Owned {
    function destroy() public virtual;
}

contract Faucet is Mortal {
    bytes32 private hashedPassword;
    bool public isWalletBlocked;

    event Withdrawal(address indexed to, uint amount);
    event Deposit(address indexed from, uint amount);
    event SentTo(address indexed to, uint amount);
    event WalletBlocked(address indexed owner);
    event WalletUnblocked(address indexed owner);
    event PasswordChanged(address indexed owner);

    constructor() public payable {
        hashedPassword = keccak256(abi.encodePacked("defaultPassword"));
        isWalletBlocked = false;
    }

    function verifyPassword(string memory password) public view returns (bool) {
        return keccak256(abi.encodePacked(password)) == hashedPassword;
    }

    function changePassword(string memory newPassword) public onlyOwner {
        hashedPassword = keccak256(abi.encodePacked(newPassword));
        emit PasswordChanged(owner);
    }

    function blockWallet() public onlyOwner {
        isWalletBlocked = true;
        emit WalletBlocked(owner);
    }

    function unblockWallet(string memory password) public onlyOwner {
        require(verifyPassword(password), "Incorrect password");
        isWalletBlocked = false;
        emit WalletUnblocked(owner);
    }

    function withdraw(uint withdraw_amount) public onlyOwner {
        require(!isWalletBlocked, "Wallet is blocked");
        require(withdraw_amount <= 0.1 ether, "Withdrawal amount exceeds limit");

        require(
            address(this).balance >= withdraw_amount,
            "Insufficient balance in faucet for withdrawal request"
        );

        msg.sender.transfer(withdraw_amount);

        emit Withdrawal(msg.sender, withdraw_amount);
    }

    function getBalance() public view returns (uint) {
        return address(this).balance;
    }

    function sendTo(address payable to, uint amount) public onlyOwner {
        require(!isWalletBlocked, "Wallet is blocked");
        require(amount <= address(this).balance, "Insufficient balance in the faucet");
        require(to != address(0), "Invalid recipient address");
        require(amount > 0, "Amount must be greater than zero");

        to.transfer(amount);

        emit SentTo(to, amount);
    }

    receive() external payable {
        emit Deposit(msg.sender, msg.value);
    }

    function destroy() public override onlyOwner {
        selfdestruct(owner);
    }
}
