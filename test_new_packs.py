from apps import APPS

# Verify all 6 new packs are registered
new_packs = [
    "ai-ethics-governance",
    "supply-chain-analyst",
    "data-scientist",
    "business-intelligence",
    "innovation-strategist",
    "devsecops",
]
for name in new_packs:
    app = APPS.get(name)
    assert app is not None, f"{name} not registered!"
    print(f"  {name}: {app.name} v{app.version} ({app.category})")

# Functional test: AI Ethics
from apps.ai_ethics_pack.schemas import (  # noqa: E402
    BiasMetric,
    EthicsConfig,
    EthicsFramework,
    EthicsOperation,
    EthicsRequest,
)
from apps.ai_ethics_pack.schemas import BusinessContext as EthicsContext  # noqa: E402

req = EthicsRequest(
    operation="bias_detection",
    business_context=EthicsContext(
        project_name="test",
        domain="finance",
        ml_use_case="credit_scoring",
        team_size=5,
        protected_attributes=[],
    ),
    inputs=EthicsConfig(
        operation=EthicsOperation.bias_detection,
        frameworks=[EthicsFramework.fairness],
        bias_metrics=[BiasMetric.demographic_parity],
    ),
)
report = APPS["ai-ethics-governance"].worker.execute(req.model_dump())
print(
    f"  AI Ethics: fairness_score={report['fairness_score']}, violations={len(report['fairness_violations'])}"  # noqa: E501
)

# Functional test: Supply Chain
from apps.supply_chain_analyst.schemas import BusinessContext as SCContext  # noqa: E402
from apps.supply_chain_analyst.schemas import (  # noqa: E402
    SupplyChainConfig,
    SupplyChainOperation,
    SupplyChainRequest,
)

req = SupplyChainRequest(
    operation="route_optimization",
    business_context=SCContext(project_name="test", domain="logistics", team_size=10),
    inputs=SupplyChainConfig(operation=SupplyChainOperation.route_optimization),
)
report = APPS["supply-chain-analyst"].worker.execute(req.model_dump())
print(
    f"  Supply Chain: optimizations={report['total_optimizations']}, savings={report['cost_savings_estimate']}"  # noqa: E501
)

# Functional test: Data Scientist
from apps.data_scientist.schemas import BusinessContext as DSContext  # noqa: E402
from apps.data_scientist.schemas import (  # noqa: E402
    DataScienceConfig,
    DataScienceOperation,
    DataScienceRequest,
    Dataset,
    FeatureConfig,
    MLAlgorithm,
    MLTask,
    ModelConfig,
)

req = DataScienceRequest(
    operation="model_training",
    business_context=DSContext(project_name="test", domain="saas", team_size=5),
    inputs=DataScienceConfig(
        operation=DataScienceOperation.model_training,
        task=MLTask.classification,
        datasets=[
            Dataset(name="d1", path="/d1.csv", n_samples=1000, n_features=10, target_column="y")
        ],
        features=[FeatureConfig(name="f1", type="numerical", transformation="scaling")],
        model=ModelConfig(
            algorithm=MLAlgorithm.random_forest,
            task=MLTask.classification,
            hyperparameters={"n_estimators": 100},
        ),
        metrics=["accuracy"],
    ),
)
report = APPS["data-scientist"].worker.execute(req.model_dump())
print(
    f"  Data Scientist: quality={report['quality_score']}, trained={len(report['training_results'])}"  # noqa: E501
)

# Functional test: Business Intelligence
from apps.business_intelligence.schemas import (  # noqa: E402
    BIConfig,
    BIReportType,
    BIRequest,
    KpiTarget,
    MetricDefinition,
    MetricType,
)
from apps.business_intelligence.schemas import BusinessContext as BIContext  # noqa: E402

req = BIRequest(
    report_type="dashboard",
    business_context=BIContext(project_name="test", domain="saas", team_size=5),
    inputs=BIConfig(
        report_type=BIReportType.dashboard,
        metrics=[
            MetricDefinition(
                id="m1",
                name="Revenue",
                type=MetricType.revenue,
                description="Monthly revenue",
                target=100000,
                unit="USD",
                aggregation="sum",
            )
        ],
        kpi_targets=[
            KpiTarget(
                metric_id="m1",
                target_value=100000,
                current_value=95000,
                threshold_warning=80000,
                threshold_critical=50000,
            )
        ],
        time_range="last_30_days",
    ),
)
report = APPS["business-intelligence"].worker.execute(req.model_dump())
print(
    f"  Business Intelligence: health={report['overall_health']}, kpis={len(report['kpi_tracking'])}"  # noqa: E501
)

# Functional test: Innovation Strategist
from apps.innovation_strategist.schemas import BusinessContext as ISContext  # noqa: E402
from apps.innovation_strategist.schemas import (  # noqa: E402
    InnovationConfig,
    InnovationOperation,
    InnovationRequest,
    TechnologyDomain,
    TrendCategory,
    TrendTimeframe,
)

req = InnovationRequest(
    operation="trend_analysis",
    business_context=ISContext(project_name="test", domain="software", team_size=5),
    inputs=InnovationConfig(
        operation=InnovationOperation.trend_analysis,
        trend_categories=[TrendCategory.emerging_technology, TrendCategory.market_dynamics],
        technology_domains=[
            TechnologyDomain(
                name="ai", description="Artificial Intelligence", maturity_level="emerging"
            )
        ],
        time_horizon=TrendTimeframe.medium_term,
    ),
)
report = APPS["innovation-strategist"].worker.execute(req.model_dump())
print(
    f"  Innovation Strategist: signals={len(report['trend_signals'])}, scenarios={len(report['scenarios'])}, opps={len(report['opportunities'])}"  # noqa: E501
)

# Functional test: DevSecOps
from apps.devsecops.schemas import BusinessContext as DSContext2  # noqa: E402
from apps.devsecops.schemas import (  # noqa: E402
    DevSecOpsConfig,
    DevSecOpsRequest,
    PipelineConfig,
    PipelineStage,
    SecurityGate,
)

req = DevSecOpsRequest(
    operation="pipeline_security_audit",
    business_context=DSContext2(project_name="test", domain="saas", team_size=8),
    inputs=DevSecOpsConfig(
        operation="pipeline_security_audit",
        pipeline=PipelineConfig(
            name="ci-cd-main",
            stages=[
                PipelineStage(
                    name="build",
                    order=1,
                    gates=[SecurityGate.sast, SecurityGate.sca, SecurityGate.secrets_detection],
                )
            ],
            compliance_standards=["soc2", "iso27001"],
        ),
        stages=[
            PipelineStage(
                name="build",
                order=1,
                gates=[SecurityGate.sast, SecurityGate.sca, SecurityGate.secrets_detection],
            )
        ],
    ),
)
report = APPS["devsecops"].worker.execute(req.model_dump())
print(
    f"  DevSecOps: gates={len(report['gate_results'])}, score={report['security_score']}, status={report['overall_status']}"  # noqa: E501
)

print()
print("All 6 packs functional test PASSED!")
