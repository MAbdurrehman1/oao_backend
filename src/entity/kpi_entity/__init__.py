from enum import Enum
from typing import Type

from .general_kpi import GeneralKPI
from .readiness_kpi import ReadinessKPI
from .execution_kpi import ExecutionKPI
from .guidance_kpi import GuidanceKPI
from .urgency_kpi import UrgencyKPI
from .empowerment_kpi import EmpowermentKPI
from .vision_kpi import VisionKPI
from .leadership_kpi import LeadershipKPI
from .wins_kpi import WinsKPI
from .info_capital_kpi import InfoCapitalKPI
from .urgency_strength_kpi import UrgencyStrengthKPI
from .urgency_patience_kpi import UrgencyPatienceKPI
from .people_readiness_kpi import PeopleReadinessKPI
from .organizational_support import OrganizationalSupportKPI
from .vision_communication_kpi import VisionCommunicationKPI
from .vision_strength_kpi import VisionStrengthKPI
from .leadership_strength_kpi import LeadershipStrengthKPI
from .incentive_systems_kpi import IncentiveSystemsKPI
from .awareness_of_successful_wins_kpi import AwarenessOfSuccessfulWinsKPI
from .pipeline_of_wins_kpi import PipelineOfWinsKPI
from .strength_of_information_capital_kpi import StrengthOfInformationCapitalKPI
from .usability_of_information_capital_kpi import UsabilityOfInformationCapitalKPI
from .abc_kpi import KPIValue, ValuedKPI, AbstractKPI


class KPIEnum(str, Enum):
    readiness: str = "READINESS"
    guidance: str = "GUIDANCE"
    execution: str = "EXECUTION"
    urgency: str = "URGENCY"
    empowerment: str = "EMPOWERMENT"
    vision: str = "VISION"
    leadership: str = "LEADERSHIP"
    wins: str = "WINS"
    info_capital: str = "INFO_CAPITAL"
    urgency_strength: str = "URGENCY_STRENGTH"
    urgency_patience: str = "URGENCY_PATIENCE"
    people_readiness: str = "PEOPLE_READINESS"
    organizational_support: str = "ORGANIZATIONAL_SUPPORT"
    vision_communication: str = "VISION_COMMUNICATION"
    vision_strength: str = "VISION_STRENGTH"
    leadership_strength: str = "LEADERSHIP_STRENGTH"
    incentive_systems: str = "INCENTIVE_SYSTEMS"
    awareness_of_successful_wins: str = "AWARENESS_OF_SUCCESSFUL_WINS"
    pipeline_of_wins: str = "PIPELINE_OF_WINS"
    strength_of_information_capital: str = "STRENGTH_OF_INFORMATION_CAPITAL"
    usability_of_information_capital: str = "USABILITY_OF_INFORMATION_CAPITAL"


KPI_MAPPING: dict[str, Type[AbstractKPI]] = {
    KPIEnum.readiness.value: ReadinessKPI,
    KPIEnum.guidance.value: GuidanceKPI,
    KPIEnum.execution.value: ExecutionKPI,
    KPIEnum.urgency: UrgencyKPI,
    KPIEnum.empowerment: EmpowermentKPI,
    KPIEnum.vision: VisionKPI,
    KPIEnum.leadership: LeadershipKPI,
    KPIEnum.wins: WinsKPI,
    KPIEnum.info_capital: InfoCapitalKPI,
    KPIEnum.urgency_strength: UrgencyStrengthKPI,
    KPIEnum.urgency_patience: UrgencyPatienceKPI,
    KPIEnum.people_readiness: PeopleReadinessKPI,
    KPIEnum.organizational_support: OrganizationalSupportKPI,
    KPIEnum.vision_communication: VisionCommunicationKPI,
    KPIEnum.vision_strength: VisionStrengthKPI,
    KPIEnum.leadership_strength: LeadershipStrengthKPI,
    KPIEnum.incentive_systems: IncentiveSystemsKPI,
    KPIEnum.awareness_of_successful_wins: AwarenessOfSuccessfulWinsKPI,
    KPIEnum.pipeline_of_wins: PipelineOfWinsKPI,
    KPIEnum.strength_of_information_capital: StrengthOfInformationCapitalKPI,
    KPIEnum.usability_of_information_capital: UsabilityOfInformationCapitalKPI,
}
PARENT_KPI_SET = [ReadinessKPI, GuidanceKPI, ExecutionKPI]
