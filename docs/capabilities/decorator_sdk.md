# Decorator SDK Capability Pack

**Version:** 1.0.0
**Target Grade:** A (≥90%)
**Status:** Implemented
**Phase:** Core Infrastructure
**RFC:** [RFC-0003](docs/rfcs/RFC-0003-decorator-sdk.md)

## Ringkasan

Decorator SDK menyediakan framework untuk mendekorasi Capability Pack BaseApp instance dengan cross-cutting concerns: logging, caching, metrics, retry, circuit breaking, dan lainnya — semuanya melalui transparent proxying. SDK ini memungkinkan developer pack untuk menambahkan perilaku silang (cross-cutting) tanpa memodifikasi kode Business Logic asli.

## Arsitektur

```
┌─────────────────────────────────────────────────────────┐
│  BaseApp (Capability Pack)                              │
│  └─ MyCapabilityPack.get_capabilities()                  │
│  └─ MyCapabilityPack.execute(task)                       │
│  └─ MyCapabilityPack.validate_input(task)                │
└──────────┬──────────────────────────────────────────────┘
           │
           ├─ ChainBuilder.add("logging")                  │
           ├─ ChainBuilder.add("caching")                  │
           ├─ ChainBuilder.add("metrics")                  │
           ├─ ChainBuilder.add("retry")                    │
           └─ ChainBuilder.add("circuit_breaker")          │
           │
           ▼
┌─────────────────────────────────────────────────────────┐
│  Decorator Chain (DecoratorBase)                        │
│  ┌─────────────┐ → ┌──────────┐ → ┌──────────┐         │
│  │ Logging     │ → │ Caching  │ → │ Metrics  │ → ...   │
│  └─────────────┘ → └──────────┘ → └──────────┘         │
│  • _before: log method call                            │
│  • _around: check cache                                │
│  • _after: record metrics                              │
│  • _on_error: log + re-raise                          │
└─────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────┐
│  Hot-Swap Manager                                        │
│  • Zero-downtime decorator replacement (< 100ms)       │
│  • Chain state persistence                              │
│  • Rollback capability                                  │
└─────────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────┐
│  Contract Validator                                      │
│  • Validates BaseApp compliance per layer              │
│  • Chain-wide validation                                │
│  • Issue reporting with fix suggestions                │
└─────────────────────────────────────────────────────────┘
```

## Decorator Tersedia

| Nama | Kelas | Deskripsi |
|---|---|---|
| `logging` | LoggingDecorator | Logs semua method invocation dengan args dan hasil |
| `caching` | CachingDecorator | Caches hasil execute() berdasarkan input hash, dengan TTL dan LRU eviction |
| `metrics` | MetricsDecorator | Mengumpulkan latency, call count, error count, dan statistik distribusi |
| `retry` | RetryDecorator | Retry dengan exponential backoff, configurable max_retries |
| `circuit_breaker` | CircuitBreakerDecorator | Circuit breaker pattern dengan CLOSED/OPEN/HALF_OPEN states |

## Augmentation Points

Decorator SDK mendukung 4 jenis hook:

1. **`before`** (`_before`): Dipanggil sebelum method wrapped dieksekusi. Contoh: logging entry.
2. **`around`** (`_around`): Membungkus pemanggilan method. Contoh: cache lookup, metrics timing.
3. **`after`** (`_after`): Dipanggil setelah method berhasil mengeksekusi. Contoh: cache store, metrics recording.
4. **`on_error`** (`_on_error`): Dipanggil ketika method melempar exception. Contoh: error logging, retry decision.

## Chain Builder

```python
from backend.app.core.decorators import ChainBuilder, DecoratorRegistry

builder = ChainBuilder()
builder.add("logging")
builder.add("caching", {"max_size": 128, "ttl": 300.0})
builder.add("metrics")
builder.add("retry", {"max_retries": 3, "base_delay": 0.1})

decorated_app = builder.build(my_base_app)
result = decorated_app.execute(task)
```

## Hot-Swap Manager

```python
from backend.app.core.decorators import HotSwapManager

manager = HotSwapManager()
# Add logging to existing chain
manager.swap("my_app", app, [("metrics", {})], ("logging", {}))
```

## API Reference

### DecoratorBase
```python
class DecoratorBase(BaseApp):
    def __init__(self, wrapped: BaseApp | None = None, config: dict[str, Any] | None = None)
    def _before(self, method_name: str, args: tuple, kwargs: dict) -> None
    def _after(self, method_name: str, args: tuple, kwargs: dict, result: Any) -> Any
    def _around(self, method_name: str, func: Callable, args: tuple, kwargs: dict) -> Any
    def _on_error(self, method_name: str, args: tuple, kwargs: dict, exc: Exception) -> Any
    def _invoke(self, method_name: str, *args, **kwargs) -> Any
```

### DecoratorRegistry
```python
class DecoratorRegistry:
    @classmethod
    def register(cls, name: str, decorator_cls: type[DecoratorBase]) -> None
    @classmethod
    def unregister(cls, name: str) -> None
    @classmethod
    def get(cls, name: str) -> type[DecoratorBase] | None
    @classmethod
    def list_available() -> list[str]
    @classmethod
    def create_decorator(cls, name: str, wrapped: BaseApp | None = None, config: dict) -> DecoratorBase | None
```

### ChainBuilder
```python
class ChainBuilder:
    def add(self, decorator_name: str, config: dict[str, Any] | None = None) -> ChainBuilder
    def add_decorator(self, decorator_cls: type[DecoratorBase], config: dict) -> ChainBuilder
    def build(self, app: BaseApp) -> DecoratorBase
    @property
    def decorator_count(self) -> int
```

### HotSwapManager
```python
class HotSwapManager:
    def swap(self, app_id: str, app: BaseApp, chain_specs: list[tuple[str, dict]], new_decorator: tuple[str, dict]) -> DecoratorBase
    def get_active(self, app_id: str) -> DecoratorBase | None
    def remove(self, app_id: str) -> bool
    @property
    def swap_count(self) -> int
```

### DecoratorContractValidator
```python
class DecoratorContractValidator:
    REQUIRED_METHODS = ["get_capabilities", "execute", "validate_input"]
    def validate(self, decorator: DecoratorBase) -> dict[str, Any]
    def validate_chain(self, decorator: DecoratorBase) -> list[dict[str, Any]]
```

## Benchmark Hasil

| Dimension | Score | Status |
|-----------|-------|--------|
| Decorator Contract | 100% | 5/5 decorators pass validation |
| Transparent Proxying | 100% | All method calls proxied correctly |
| Chain Composition | 100% | 2 and 3 decorator chains tested |
| Contract Validation | 100% | Validator accuracy verified |
| Wrapping Overhead (P95) | < 1ms | Well under 10ms threshold |
| Augmentation Isolation | 100% | Hooks don't alter results |
| Hot-Swap Success | 100% | 30/30 swaps successful |
| Hot-Swap Latency | < 5ms | Well under 100ms threshold |
| **Overall** | **100%** | ✅ **PASS** |

## Real Cases

30 kasus nyata tersedia di `real_cases/core/decorator_sdk/`:
- **dec_001–003**: LoggingDecorator (basic, error, async)
- **dec_004–006**: CachingDecorator (hit/miss, TTL, max_size)
- **dec_007–009**: MetricsDecorator (latency, errors, reset)
- **dec_010–012**: RetryDecorator (success after retry, max retries, backoff)
- **dec_013–015**: CircuitBreakerDecorator (closed, open, half-open)
- **dec_016–018**: ChainBuilder (2 decorators, 3 decorators, call order)
- **dec_019–021**: HotSwapManager (basic swap, latency, chain preservation)
- **dec_022–024**: ContractValidator (compliant, non-compliant, chain)
- **dec_025–027**: Transparency (execute, validate, capabilities)
- **dec_028–030**: Augmentation Points (before/after, around, on_error)

## Integration

```python
# Register a custom decorator
from backend.app.core.decorators import DecoratorBase, DecoratorRegistry


class RateLimitDecorator(DecoratorBase):
    name = "rate_limit"
    version = "1.0.0"
    # ... implementation ...


DecoratorRegistry.register("rate_limit", RateLimitDecorator)

# Use in a capability pack
builder = ChainBuilder()
builder.add("rate_limit", {"max_calls": 100, "window": 60})
builder.add("logging")
decorated = builder.build(MyCapabilityPack())
```
