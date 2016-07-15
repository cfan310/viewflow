from viewflow import flow, this, Flow
from viewflow.flow.views import StartFlowView

from . import models, views
from .nodes import DynamicSplit


class DynamicSplitFlow(Flow):
    """
    Dynamic split

    Depends on initial decision, several instances on make_decision task would be instantiated
    """
    process_cls = models.DynamicSplitProcess

    summary_template = """
    Decision on: {{ process.question }}<br/>
    {{ process.decision_set.count }}  of {{ process.split_count }} completed
    """

    start = (
        flow.Start(
            StartFlowView,
            fields=['question', 'split_count'],
            task_result_summary="Asks for {{ process.split_count }} decisions")
        .Permission(auto_create=True)
        .Next(this.spit_on_decision)
    )

    spit_on_decision = (
        DynamicSplit(lambda p: p.split_count)
        .Next(this.make_decision)
    )

    make_decision = (
        flow.View(
            views.DecisionView,
            task_description="Decision required")
        .Next(this.join_on_decision)
    )

    join_on_decision = flow.Join().Next(this.end)

    end = flow.End()
