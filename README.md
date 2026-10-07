# Origin Protocol — Immunefi Bug Bounty

Scope: https://immunefi.com/bug-bounty/originprotocol/scope/

## Source snapshots (shallow clone, 2026-10-07)

| Dir | Upstream | Branch | Commit |
|-----|----------|--------|--------|
| `origin-dollar/` | https://github.com/OriginProtocol/origin-dollar — OUSD / OETH / superOETHb | master | `ae82163b1c64253adad281e105ca0a774639c05f` |
| `arm-oeth/` | https://github.com/OriginProtocol/arm-oeth — ARM (Automated Redemption Manager) | main | `38660e16683980ce232cae16393ca30d20dd6d72` |
| `ousd-governance/` | https://github.com/OriginProtocol/ousd-governance — Governance / xOGN | master | `eff0d3d8221b5e1bbb3b6aacb5a1cfdd8626102a` |

Notes:
- Nested `.git` removed; ousd-governance submodules (OZ, forge-std, prb-math, ds-test) are not vendored — run `forge install` as needed.
- Large JSON claim data in ousd-governance is excluded via `.gitignore`.

## Deployed sources

`deployed/` contains the verified on-chain source of all in-scope contracts (proxy + current implementation). See [deployed/README.md](deployed/README.md) for the asset → contract mapping.

## In-scope assets (Smart Contracts)

| Name | Address |
|------|---------|
| OUSD Morpho V2 CrossChain Master Strategy | https://etherscan.io/address/0xB1d624fc40824683e2bFBEfd19eB208DbBE00866 |
| OUSD Morpho V2 CrossChain Remote Strategy | https://basescan.org/address/0xB1d624fc40824683e2bFBEfd19eB208DbBE00866 |
| Compounding Staking Strategy View | https://etherscan.io/address/0xb7992eFDa9aBBaC3522336A626191D198fa37145 |
| Compounding Staking Strategy | https://etherscan.io/address/0x25e1d468B14005716111d5e8464573e5135275f4 |
| Ethena ARM | https://etherscan.io/address/0xCEDa2d856238aA0D12f6329de20B9115f07C366d |
| Ethena ARM Aave Strategy | https://etherscan.io/address/0x0DC20109Ea012f050BeDA184844c1eD5ec6dA33A#readProxyContract |
| Wrapped Super OETH | https://basescan.org/address/0x7FcD174E80f264448ebeE8c88a7C4476AAF58Ea6#code |
| OUSD Token | https://etherscan.io/address/0x2A8e1E676Ec238d8A992307B495b45B3fEAa5e86 |
| WOUSD Token | https://etherscan.io/address/0xD2af830E8CBdFed6CC11Bab697bB25496ed6FA62 |
| OUSD Vault | https://etherscan.io/address/0xE75D77B1865Ae93c7eaa3040B038D7aA7BC02F70 |
| OUSD Strategy - Curve AMO | https://etherscan.io/address/0x26a02ec47ACC2A3442b757F45E0A82B8e993Ce11 |
| OUSD Strategy - Morpho V2 | https://etherscan.io/address/0x3643cafA6eF3dd7Fcc2ADaD1cabf708075AFFf6e |
| OUSD Strategy - Base CrossChain Master | https://etherscan.io/address/0xB1d624fc40824683e2bFBEfd19eB208DbBE00866 |
| OUSD Strategy - Base CrossChain Remote | https://basescan.org/address/0xB1d624fc40824683e2bFBEfd19eB208DbBE00866 |
| OUSD Strategy - HyperEVM CrossChain Master | https://etherscan.io/address/0xE0228DB13F8C4Eb00fD1e08e076b09eF5cD0EA1e |
| OUSD Strategy - HyperEVM CrossChain Remote | https://hyperevmscan.io/address/0xE0228DB13F8C4Eb00fD1e08e076b09eF5cD0EA1e |
| OUSD CoW Harvester | https://etherscan.io/address/0xD400341aEfED0BC75176714cFdE82e8BDAA2D3b8 |
| OETH Token | https://etherscan.io/address/0x856c4Efb76C1D1AE02e20CEB03A2A6a08b0b8dC3 |
| WOETH Token | https://etherscan.io/address/0xDcEe70654261AF21C44c093C300eD3Bb97b78192 |
| OETH Vault | https://etherscan.io/address/0x39254033945AA2E4809Cc2977E7087BEE48bd7Ab |
| OETH Strategy - Curve AMO | https://etherscan.io/address/0xba0e352AB5c13861C26e4E773e7a833C3A223FE6 |
| OETH Strategy - Compounding Staking SSV | https://etherscan.io/address/0x25e1d468B14005716111d5e8464573e5135275f4 |
| OETH Strategy - BeaconProofs | https://etherscan.io/address/0xc4444C5D9e7C1a5A0a01c5E4b11692d589DcAF22 |
| OETH Zapper | https://etherscan.io/address/0xDA0485c1E74A7ef690E99D8286C243942eDAa07B |
| WOETH CCIP Zapper | https://etherscan.io/address/0x438731b5Ee8fEcC02a28532713E237b93260C3F8 |
| Bridged WOETH | https://arbiscan.io/address/0xD8724322f44E5c58D7A815F542036fb17DbbF839 |
| Bridged WOETH | https://basescan.org/address/0xD8724322f44E5c58D7A815F542036fb17DbbF839 |
| superOETHb Token | https://basescan.org/address/0xDBFeFD2e8460a6Ee4955A68582F85708BAEA60A3 |
| wsuperOETHb Token | https://basescan.org/address/0x7FcD174E80f264448ebeE8c88a7C4476AAF58Ea6 |
| superOETHb Vault | https://basescan.org/address/0x98a0CbeF61bD2D21435f433bE4CD42B56B38CC93 |
| wsuperOETHb bridged strategy | https://basescan.org/address/0x80c864704DD06C3693ed5179190786EE38ACf835 |
| superOETHb Strategy - Aerodrome AMO | https://basescan.org/address/0xF611cC500eEE7E4e4763A05FE623E2363c86d2Af |
| superOETHb Strategy - Curve AMO | https://basescan.org/address/0x9cfcAF81600155e01c63e4D2993A8A81A8205829 |
| superOETHb Harvester | https://basescan.org/address/0x0CbEAcf86232fC04050cD679d860516F7254c22E |
| superOETHb Zapper | https://basescan.org/address/0x3b56c09543D3068f8488ED34e6F383c3854d2bC1 |
| WETH ARM | https://etherscan.io/address/0x68025A4615407993A680102b08a23A61D11C657C |
| WETH ARM - stETH Adapter | https://etherscan.io/address/0x7b0a90552D2dc01936301A45bFC813717Af7E8a9 |
| WETH ARM - wstETH Adapter | https://etherscan.io/address/0xE28ca056A12134b6B872D1CbE04cd1A82fDfeA95 |
| WETH ARM - eETH Adapter | https://etherscan.io/address/0xFa205c9a110a3e82Bd8d223CccCB15C5b9E6434e |
| WETH ARM - weETH Adapter | https://etherscan.io/address/0xD5F61bFd890169c28858039f6b6c9b517407C852 |
| WETH ARM - MorphoMarket | https://etherscan.io/address/0xe192824f42ae3D643ac867774b45E8d233d86c72 |
| WETH ARM Zapper | https://etherscan.io/address/0xE11EDbd5AE4Fa434Af7f8D7F03Da1742996e7Ab2 |
| USDC ARM | https://etherscan.io/address/0x9E3A7026E5767F2d7Ff5e83b0ed011005f45a170 |
| USDC ARM CapManager | https://etherscan.io/address/0x19B1Edb2caD902F103a20A30011f125DCe44F954 |
| USDC ARM - PYUSD Adapter | https://etherscan.io/address/0x0C9ac6D63B2b2A1b502E29eC47a53d0966Ea9465 |
| USDC ARM - USDG Adapter | https://etherscan.io/address/0xAb98aC901B8A26636d9cf3Cf38d9aCdcD045788f |
| USDC ARM - AAVE Market | https://etherscan.io/address/0x43f35Fa72dcf93DaD9843Ab7B0E0587bF57d9643 |
| Ethena ARM - sUSDe Adapter | https://etherscan.io/address/0xE620aFB67223AE03C260112aE21A717Af94C90f0 |
| Ethena ARM - AAVE Market | https://etherscan.io/address/0x0DC20109Ea012f050BeDA184844c1eD5ec6dA33A |
| Ethena ARM Unstaker | https://etherscan.io/address/0xB1b9cf49B16DECc1634AEa0675C3b976FfE2B4F4 |
| Lido ARM | https://etherscan.io/address/0x85B78AcA6Deae198fBF201c82DAF6Ca21942acc6 |
| Lido ARM - Morpho Market | https://etherscan.io/address/0xB7CeFE4CB483Be80C2963D3D9Edb991e69ff39cf |
| Lido ARM Zapper | https://etherscan.io/address/0x01F30B7358Ba51f637d1aa05D9b4A60f76DAD680 |
| Origin Timelock | https://etherscan.io/address/0x35918cDE7233F2dD33fA41ae3Cb6aE0e42E0e69F |
| Origin Governance | https://etherscan.io/address/0x1D3Fbd4d129Ddd2372EA85c5Fa00b2682081c9EC |
| xOGN | https://etherscan.io/address/0x63898b3b6Ef3d39332082178656E9862bee45C57 |
| Base Timelock | https://basescan.org/address/0xf817cb3092179083c48c014688D98B72fB61464f |
| HyperEVM Timelock | https://hyperevmscan.io/address/0x77121911A387c9e4Eae46345E0f831A6da8a1364 |
| SafeModule - OUSD AutoWithdrawal | https://etherscan.io/address/0x90d588fc0eC3DB9c4b417dB4537fE08e063D2ae5 |
| SafeModule - Claim Strategy Rewards | https://etherscan.io/address/0x1b84E64279D63f48DdD88B9B2A7871e817152A44 |
| OETH Vault Lens | https://etherscan.io/address/0xad2b1657E2c3243750B32Cb9A51169575945b05B |

Primacy of Impact also applies. Website in scope: https://app.originprotocol.com/
