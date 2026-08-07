// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import {IERC20Metadata} from "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol";
import {SafeERC20} from "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {Ownable2Step} from "@openzeppelin/contracts/access/Ownable2Step.sol";
import {Pausable} from "@openzeppelin/contracts/utils/Pausable.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

import {JWIS} from "./JWIS.sol";

/// @title JAYWISDOM CLARITY Engine
/// @notice Escrows USD-stablecoin service payments, settles Jay's treasury on
/// valid CLARITY fulfillment, mints capped JWIS rewards, and exposes replay hashes.
contract ClarityEngine is Ownable2Step, Pausable, ReentrancyGuard {
    using SafeERC20 for IERC20;

    enum ServiceType {
        CLARITY_RUBRIC,
        ENS_ENABLEMENT_LESSON,
        GUIDED_REPLAY,
        ENABLEMENT_AUDIT
    }

    enum OrderStatus {
        NONE,
        PAID,
        FULFILLED,
        REFUNDED
    }

    enum FindingState {
        COMPLETE,
        INCOMPLETE,
        BLOCKED,
        ESCALATION_REQUIRED
    }

    enum ReplayComparison {
        NOT_READY,
        MATCH,
        DIVERGE
    }

    struct ServiceConfig {
        uint96 price;
        uint128 jwisReward;
        bool enabled;
    }

    struct ClarityCommitment {
        bytes32 controllingAuthority;
        bytes32 lawfulPurpose;
        bytes32 responsibleActor;
        bytes32 requiredEvidence;
        bytes32 instrumentsEnablements;
        bytes32 trackingCustody;
        bytes32 remedyAppeal;
    }

    struct Order {
        address customer;
        address settlementTreasury;
        uint64 createdAt;
        uint64 deadline;
        uint96 amount;
        ServiceType serviceType;
        OrderStatus status;
        FindingState findingState;
        uint8 clarityScore;
        uint128 jwisRewardPromised;
        uint128 jwisRewardMinted;
        bytes32 rubricVersion;
        bytes32 questionHash;
        bytes32 clarityHash;
        bytes32 resultHash;
        bytes32 humanUriHash;
        bytes32 machineUriHash;
        bytes32 replayHash;
    }

    IERC20Metadata public immutable paymentToken;
    JWIS public immutable jwisToken;

    address public treasury;
    address public fulfiller;
    bytes32 public rubricVersion;
    uint64 public fulfillmentWindow;
    uint256 public nextOrderId = 1;

    mapping(ServiceType => ServiceConfig) private _serviceConfigs;
    mapping(uint256 => Order) private _orders;

    error InvalidAddress();
    error UnsupportedPaymentDecimals(uint8 observed);
    error InvalidFulfillmentWindow();
    error InvalidQuestionHash();
    error ServiceDisabled();
    error OrderNotPaid();
    error NotCustomer();
    error NotFulfiller();
    error FulfillmentExpired();
    error RefundNotAvailable();
    error MissingClarityField(uint8 fieldIndex);
    error InvalidResultHash();
    error InvalidUriHash();
    error InvalidServiceConfig();
    error InvalidRubricVersion();

    event ServiceConfigured(
        ServiceType indexed serviceType,
        uint96 price,
        uint128 jwisReward,
        bool enabled
    );
    event TreasuryUpdated(address indexed previousTreasury, address indexed newTreasury);
    event FulfillerUpdated(address indexed previousFulfiller, address indexed newFulfiller);
    event RubricVersionUpdated(bytes32 indexed previousVersion, bytes32 indexed newVersion);
    event FulfillmentWindowUpdated(uint64 previousWindow, uint64 newWindow);

    event ServicePurchased(
        uint256 indexed orderId,
        address indexed customer,
        ServiceType indexed serviceType,
        uint96 amount,
        bytes32 questionHash,
        uint64 deadline
    );

    event DualDelivery(
        uint256 indexed orderId,
        address indexed customer,
        bytes32 indexed replayHash,
        bytes32 humanUriHash,
        bytes32 machineUriHash,
        bytes32 resultHash,
        uint8 clarityScore,
        FindingState findingState
    );

    event RevenueSettled(
        uint256 indexed orderId,
        address indexed treasury,
        uint96 paymentAmount,
        uint128 jwisRewardMinted
    );

    event OrderRefunded(uint256 indexed orderId, address indexed customer, uint96 amount);

    constructor(
        address paymentToken_,
        address initialOwner_,
        address treasury_,
        address fulfiller_,
        bytes32 rubricVersion_
    ) Ownable(initialOwner_) {
        if (
            paymentToken_ == address(0) || initialOwner_ == address(0)
                || treasury_ == address(0) || fulfiller_ == address(0)
        ) revert InvalidAddress();

        uint8 decimals = IERC20Metadata(paymentToken_).decimals();
        if (decimals != 6) revert UnsupportedPaymentDecimals(decimals);

        paymentToken = IERC20Metadata(paymentToken_);
        treasury = treasury_;
        fulfiller = fulfiller_;
        if (rubricVersion_ == bytes32(0)) revert InvalidRubricVersion();
        rubricVersion = rubricVersion_;
        fulfillmentWindow = 24 hours;

        jwisToken = new JWIS(address(this));

        _configureService(ServiceType.CLARITY_RUBRIC, 1_000_000, 1 ether, true);
        _configureService(ServiceType.ENS_ENABLEMENT_LESSON, 5_000_000, 5 ether, true);
        _configureService(ServiceType.GUIDED_REPLAY, 10_000_000, 10 ether, true);
        _configureService(ServiceType.ENABLEMENT_AUDIT, 25_000_000, 25 ether, true);
    }

    modifier onlyFulfiller() {
        if (msg.sender != fulfiller) revert NotFulfiller();
        _;
    }

    function purchase(ServiceType serviceType, bytes32 questionHash)
        external
        nonReentrant
        whenNotPaused
        returns (uint256 orderId)
    {
        if (questionHash == bytes32(0)) revert InvalidQuestionHash();

        ServiceConfig memory config = _serviceConfigs[serviceType];
        if (!config.enabled) revert ServiceDisabled();

        orderId = nextOrderId++;
        uint64 createdAt = uint64(block.timestamp);
        uint64 deadline = createdAt + fulfillmentWindow;

        _orders[orderId] = Order({
            customer: msg.sender,
            settlementTreasury: treasury,
            createdAt: createdAt,
            deadline: deadline,
            amount: config.price,
            serviceType: serviceType,
            status: OrderStatus.PAID,
            findingState: FindingState.INCOMPLETE,
            clarityScore: 0,
            jwisRewardPromised: config.jwisReward,
            jwisRewardMinted: 0,
            rubricVersion: rubricVersion,
            questionHash: questionHash,
            clarityHash: bytes32(0),
            resultHash: bytes32(0),
            humanUriHash: bytes32(0),
            machineUriHash: bytes32(0),
            replayHash: bytes32(0)
        });

        IERC20(address(paymentToken)).safeTransferFrom(msg.sender, address(this), config.price);

        emit ServicePurchased(
            orderId,
            msg.sender,
            serviceType,
            config.price,
            questionHash,
            deadline
        );
    }

    function fulfill(
        uint256 orderId,
        ClarityCommitment calldata clarity,
        bytes32 resultHash,
        bytes32 humanUriHash,
        bytes32 machineUriHash,
        FindingState findingState
    ) external nonReentrant whenNotPaused onlyFulfiller returns (bytes32 replayHash) {
        Order storage order = _orders[orderId];
        if (order.status != OrderStatus.PAID) revert OrderNotPaid();
        if (block.timestamp > order.deadline) revert FulfillmentExpired();
        if (resultHash == bytes32(0)) revert InvalidResultHash();
        if (humanUriHash == bytes32(0) || machineUriHash == bytes32(0)) {
            revert InvalidUriHash();
        }

        _enforceClarityGate(clarity);

        bytes32 clarityHash = keccak256(abi.encode(clarity));
        replayHash = _computeReplayHash(
            orderId,
            order.customer,
            order.serviceType,
            order.rubricVersion,
            order.questionHash,
            clarityHash,
            resultHash,
            humanUriHash,
            machineUriHash,
            findingState
        );

        order.status = OrderStatus.FULFILLED;
        order.findingState = findingState;
        order.clarityScore = 100;
        order.clarityHash = clarityHash;
        order.resultHash = resultHash;
        order.humanUriHash = humanUriHash;
        order.machineUriHash = machineUriHash;
        order.replayHash = replayHash;

        uint128 reward = order.jwisRewardPromised;
        if (jwisToken.totalSupply() + reward <= jwisToken.cap()) {
            jwisToken.mint(order.customer, reward);
            order.jwisRewardMinted = reward;
        } else {
            reward = 0;
        }

        IERC20(address(paymentToken)).safeTransfer(order.settlementTreasury, order.amount);

        emit DualDelivery(
            orderId,
            order.customer,
            replayHash,
            humanUriHash,
            machineUriHash,
            resultHash,
            100,
            findingState
        );
        emit RevenueSettled(orderId, order.settlementTreasury, order.amount, reward);
    }

    function refund(uint256 orderId) external nonReentrant {
        Order storage order = _orders[orderId];
        if (order.status != OrderStatus.PAID) revert OrderNotPaid();
        if (msg.sender != order.customer) revert NotCustomer();
        if (block.timestamp <= order.deadline) revert RefundNotAvailable();

        order.status = OrderStatus.REFUNDED;
        IERC20(address(paymentToken)).safeTransfer(order.customer, order.amount);

        emit OrderRefunded(orderId, order.customer, order.amount);
    }

    function verifyReplay(
        uint256 orderId,
        ClarityCommitment calldata clarity,
        bytes32 resultHash,
        bytes32 humanUriHash,
        bytes32 machineUriHash,
        FindingState findingState
    ) external view returns (ReplayComparison) {
        Order storage order = _orders[orderId];
        if (order.status != OrderStatus.FULFILLED) return ReplayComparison.NOT_READY;

        bytes32 observed = _computeReplayHash(
            orderId,
            order.customer,
            order.serviceType,
            order.rubricVersion,
            order.questionHash,
            keccak256(abi.encode(clarity)),
            resultHash,
            humanUriHash,
            machineUriHash,
            findingState
        );

        return observed == order.replayHash ? ReplayComparison.MATCH : ReplayComparison.DIVERGE;
    }

    function getOrder(uint256 orderId) external view returns (Order memory) {
        return _orders[orderId];
    }

    function getServiceConfig(ServiceType serviceType)
        external
        view
        returns (ServiceConfig memory)
    {
        return _serviceConfigs[serviceType];
    }

    function configureService(
        ServiceType serviceType,
        uint96 price,
        uint128 jwisReward,
        bool enabled
    ) external onlyOwner {
        _configureService(serviceType, price, jwisReward, enabled);
    }

    function setTreasury(address newTreasury) external onlyOwner {
        if (newTreasury == address(0)) revert InvalidAddress();
        address previous = treasury;
        treasury = newTreasury;
        emit TreasuryUpdated(previous, newTreasury);
    }

    function setFulfiller(address newFulfiller) external onlyOwner {
        if (newFulfiller == address(0)) revert InvalidAddress();
        address previous = fulfiller;
        fulfiller = newFulfiller;
        emit FulfillerUpdated(previous, newFulfiller);
    }

    function setRubricVersion(bytes32 newVersion) external onlyOwner {
        if (newVersion == bytes32(0)) revert InvalidRubricVersion();
        bytes32 previous = rubricVersion;
        rubricVersion = newVersion;
        emit RubricVersionUpdated(previous, newVersion);
    }

    function setFulfillmentWindow(uint64 newWindow) external onlyOwner {
        if (newWindow < 5 minutes || newWindow > 30 days) revert InvalidFulfillmentWindow();
        uint64 previous = fulfillmentWindow;
        fulfillmentWindow = newWindow;
        emit FulfillmentWindowUpdated(previous, newWindow);
    }

    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }

    function _configureService(
        ServiceType serviceType,
        uint96 price,
        uint128 jwisReward,
        bool enabled
    ) internal {
        if (price == 0 || jwisReward == 0) revert InvalidServiceConfig();
        _serviceConfigs[serviceType] = ServiceConfig({
            price: price,
            jwisReward: jwisReward,
            enabled: enabled
        });
        emit ServiceConfigured(serviceType, price, jwisReward, enabled);
    }

    function _enforceClarityGate(ClarityCommitment calldata clarity) internal pure {
        if (clarity.controllingAuthority == bytes32(0)) revert MissingClarityField(0);
        if (clarity.lawfulPurpose == bytes32(0)) revert MissingClarityField(1);
        if (clarity.responsibleActor == bytes32(0)) revert MissingClarityField(2);
        if (clarity.requiredEvidence == bytes32(0)) revert MissingClarityField(3);
        if (clarity.instrumentsEnablements == bytes32(0)) revert MissingClarityField(4);
        if (clarity.trackingCustody == bytes32(0)) revert MissingClarityField(5);
        if (clarity.remedyAppeal == bytes32(0)) revert MissingClarityField(6);
    }

    function _computeReplayHash(
        uint256 orderId,
        address customer,
        ServiceType serviceType,
        bytes32 orderRubricVersion,
        bytes32 questionHash,
        bytes32 clarityHash,
        bytes32 resultHash,
        bytes32 humanUriHash,
        bytes32 machineUriHash,
        FindingState findingState
    ) internal view returns (bytes32) {
        return keccak256(
            abi.encode(
                "JAYWISDOM_REPLAY_V0_1",
                block.chainid,
                address(this),
                orderRubricVersion,
                orderId,
                customer,
                serviceType,
                questionHash,
                clarityHash,
                resultHash,
                humanUriHash,
                machineUriHash,
                findingState
            )
        );
    }
}
