// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title  PatientRecordContract
 * @notice Manages patient records on Ethereum (sanitised copy for showcase).
 */
contract PatientRecordContract {

    address public owner;
    uint256 public totalRecords;
    mapping(address => bool) public authorisedProviders;

    struct PatientRecord {
        uint256 id;
        string  patientName;
        string  diagnosis;
        string  treatment;
        address currentProvider;
        bool    exists;
    }

    mapping(uint256 => PatientRecord) private records;

    event ProviderAuthorised(address indexed provider);
    event ProviderRevoked(address indexed provider);
    event RecordAdded(uint256 indexed recordId, string patientName, address indexed provider);
    event RecordTransferred(uint256 indexed recordId, address indexed from, address indexed to);

    modifier onlyOwner() {
        require(msg.sender == owner, "Caller is not the contract owner");
        _;
    }

    modifier onlyAuthorisedProvider() {
        require(authorisedProviders[msg.sender], "Caller is not an authorised provider");
        _;
    }

    constructor() {
        owner = msg.sender;
        authorisedProviders[msg.sender] = true;
        emit ProviderAuthorised(msg.sender);
    }

    function authoriseProvider(address _provider) external onlyOwner {
        require(_provider != address(0), "Invalid address");
        require(!authorisedProviders[_provider], "Provider already authorised");
        authorisedProviders[_provider] = true;
        emit ProviderAuthorised(_provider);
    }

    function revokeProvider(address _provider) external onlyOwner {
        require(authorisedProviders[_provider], "Provider is not authorised");
        authorisedProviders[_provider] = false;
        emit ProviderRevoked(_provider);
    }

    function addRecord(
        string calldata _patientName,
        string calldata _diagnosis,
        string calldata _treatment
    )
        external
        onlyAuthorisedProvider
        returns (uint256 newId)
    {
        require(bytes(_patientName).length > 0, "Patient name required");
        require(bytes(_diagnosis).length > 0,   "Diagnosis required");

        totalRecords += 1;
        newId = totalRecords;

        records[newId] = PatientRecord({
            id:              newId,
            patientName:     _patientName,
            diagnosis:       _diagnosis,
            treatment:       _treatment,
            currentProvider: msg.sender,
            exists:          true
        });

        emit RecordAdded(newId, _patientName, msg.sender);
    }

    function transferRecord(uint256 _recordId, address _newProvider) external {
        require(records[_recordId].exists, "Record does not exist");
        require(
            records[_recordId].currentProvider == msg.sender,
            "Only current provider can transfer"
        );
        require(authorisedProviders[_newProvider], "New provider is not authorised");
        require(_newProvider != msg.sender, "Cannot transfer to yourself");

        address previousProvider = records[_recordId].currentProvider;
        records[_recordId].currentProvider = _newProvider;

        emit RecordTransferred(_recordId, previousProvider, _newProvider);
    }

    function getRecord(uint256 _recordId)
        external
        view
        returns (
            uint256 id,
            string memory patientName,
            string memory diagnosis,
            string memory treatment,
            address currentProvider
        )
    {
        require(records[_recordId].exists, "Record does not exist");
        PatientRecord storage r = records[_recordId];
        return (r.id, r.patientName, r.diagnosis, r.treatment, r.currentProvider);
    }

    function isAuthorised(address _provider) external view returns (bool) {
        return authorisedProviders[_provider];
    }
}
