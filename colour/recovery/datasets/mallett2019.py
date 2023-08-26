"""
Mallett and Yuksel (2019) - Reflectance Recovery
================================================

Defines the datasets for reflectance recovery using *Mallett and Yuksel
(2019)* method.

References
----------
-   :cite:`Mallett2019` : Mallett, I., & Yuksel, C. (2019). Spectral Primary
    Decomposition for Rendering with sRGB Reflectance. Eurographics Symposium
    on Rendering - DL-Only and Industry Track, 7 pages. doi:10.2312/SR.20191216
"""

from __future__ import annotations

import numpy as np

from colour.colorimetry import MultiSpectralDistributions, SpectralShape
from colour.hints import NDArrayFloat

__author__ = "Colour Developers"
__copyright__ = "Copyright 2013 Colour Developers"
__license__ = "BSD-3-Clause - https://opensource.org/licenses/BSD-3-Clause"
__maintainer__ = "Colour Developers"
__email__ = "colour-developers@colour-science.org"
__status__ = "Production"

__all__ = [
    "SPECTRAL_SHAPE_sRGB_MALLETT2019",
    "DATA_BASIS_FUNCTIONS_sRGB_MALLETT2019",
    "MSDS_BASIS_FUNCTIONS_sRGB_MALLETT2019",
]

SPECTRAL_SHAPE_sRGB_MALLETT2019: SpectralShape = SpectralShape(380, 780, 5)
SPECTRAL_SHAPE_sRGB_MALLETT2019.__doc__ = """
Shape for *Mallett and Yuksel (2019)* *sRGB* colourspace basis functions:
(380, 780, 5).

References
----------
:cite:`Mallett2019`
"""

DATA_BASIS_FUNCTIONS_sRGB_MALLETT2019: NDArrayFloat = np.array(
    [
        [0.32745741382705500, 0.33186171308587400, 0.34068079154805200],
        [0.32375057827054100, 0.32968818775939900, 0.34656118662485200],
        [0.31343946125157700, 0.32786002162469700, 0.35870049314035100],
        [0.28887938275526500, 0.31917358023175600, 0.39194702658819500],
        [0.23920568115888600, 0.29432258369484200, 0.46647173058733300],
        [0.18970203689053500, 0.25869706476873600, 0.55160089559860200],
        [0.12174606795921800, 0.18889431925476500, 0.68935961094892800],
        [0.07457827066946600, 0.12538838199168900, 0.80003334687860700],
        [0.04443315863403370, 0.07868706031062170, 0.87687978093531400],
        [0.02892863212850290, 0.05314327086594530, 0.91792809744395500],
        [0.02231665348475120, 0.04228814603134210, 0.93539520066963200],
        [0.01691130729263180, 0.03331834550291710, 0.94977034711518300],
        [0.01418110711796670, 0.02975594818597240, 0.95606294480524000],
        [0.01305314267748730, 0.03033125053690470, 0.95661560689031600],
        [0.01198616362784500, 0.03098857189730070, 0.95702526493132800],
        [0.01128871471240480, 0.03168635518883810, 0.95702493053471300],
        [0.01090606646565170, 0.03466996150299740, 0.95442397273706600],
        [0.01040071348100420, 0.03455195744367500, 0.95504732902020400],
        [0.01063736025414650, 0.04068480619482970, 0.94867783309333400],
        [0.01090766253377410, 0.05446003736940560, 0.93463229984232800],
        [0.01103271244809880, 0.08090528742047370, 0.90806199985226900],
        [0.01131065659122680, 0.14634830285704400, 0.84234103946372700],
        [0.01115464205694030, 0.37967964329661700, 0.60916571536564700],
        [0.01014877040621220, 0.76674426865403300, 0.22310696095953300],
        [0.00891858211883843, 0.87621474761337000, 0.11486667029133600],
        [0.00768557633847106, 0.91849165561384300, 0.07382276789574370],
        [0.00670570828469526, 0.94065556253443700, 0.05263872879105550],
        [0.00599580598764424, 0.95373188453302000, 0.04027230901688870],
        [0.00553725664234189, 0.96164327984023800, 0.03281946265095910],
        [0.00519378424120663, 0.96720001968507800, 0.02760619592704560],
        [0.00502536226522334, 0.97098974639004600, 0.02398489112703940],
        [0.00513636276967508, 0.97285230356355400, 0.02201133335279220],
        [0.00543320026053983, 0.97311659407644400, 0.02145020525599660],
        [0.00581998590243535, 0.97335106915414300, 0.02082894450956850],
        [0.00640057277462412, 0.97335111554436900, 0.02024831138880870],
        [0.00744952868340878, 0.97226107973172500, 0.02028939145120660],
        [0.00858363581937657, 0.97335102174691700, 0.01806534233591300],
        [0.01039576246516740, 0.97314849518569300, 0.01645574223446850],
        [0.01356543353864920, 0.97106130630091400, 0.01537326013409550],
        [0.01938451583997420, 0.96637130595518300, 0.01424417848455170],
        [0.03208407120200240, 0.95494196750254800, 0.01297396155433470],
        [0.07435603784594110, 0.91357898955126100, 0.01206497413452180],
        [0.62439372417807500, 0.36434880390768700, 0.01125747816039010],
        [0.91831003276872000, 0.07150724254088510, 0.01018272467169420],
        [0.94925303017505100, 0.04123043447137510, 0.00951653538723741],
        [0.95818783332924600, 0.03242387418366850, 0.00938829272866817],
        [0.95818775133269800, 0.03192462979820030, 0.00988761909067028],
        [0.95818762508778200, 0.03127603317309690, 0.01053634200645890],
        [0.95567906077174600, 0.03263037042905740, 0.01169056883744480],
        [0.95800615489342900, 0.02953087214907390, 0.01246297288710370],
        [0.95410157345656400, 0.03156176117024640, 0.01433666517742030],
        [0.94760760623723700, 0.03567421827082040, 0.01671817532754430],
        [0.93868132844754900, 0.04140300539556730, 0.01991566607500250],
        [0.92446668275143400, 0.05060426044895610, 0.02492905616328100],
        [0.90460602533305600, 0.06343430038170030, 0.03195967358604020],
        [0.88041219892793300, 0.07891824529392290, 0.04066955409524840],
        [0.84778787315170000, 0.09954274266537470, 0.05266938242193960],
        [0.80577912662301900, 0.12559576009328700, 0.06862511051419470],
        [0.75253185387142100, 0.15759091044168000, 0.08987723230001360],
        [0.68643939684457800, 0.19539823904421000, 0.11816235892643400],
        [0.61869457086061000, 0.23147447477217800, 0.14983094744213300],
        [0.54026444395911100, 0.26885213609526200, 0.19088340934183400],
        [0.47296441629383800, 0.29602916421792800, 0.23100640302521700],
        [0.43270159670404900, 0.30975499444194500, 0.25754338542220200],
        [0.40535804552839200, 0.31781588338382200, 0.27682603872153600],
        [0.38549183497490200, 0.32299034738989800, 0.29151777281079500],
        [0.37098358455106100, 0.32635384793800900, 0.30266250608323300],
        [0.35760870152308100, 0.32914390227898000, 0.31324730130288600],
        [0.34871280010839300, 0.33080872680368200, 0.32047832512463300],
        [0.34488011934469100, 0.33148268992224300, 0.32363699470796100],
        [0.34191787732329100, 0.33198455035238900, 0.32609730884690000],
        [0.33953109298712900, 0.33234117252254500, 0.32812736934018400],
        [0.33716950377436700, 0.33291200941553900, 0.32991797595888800],
        [0.33617201852771700, 0.33291927969521400, 0.33090790121664900],
        [0.33516744343336300, 0.33302767257885600, 0.33180363309599500],
        [0.33442162530646300, 0.33317970467326000, 0.33239662725536100],
        [0.33400876037640200, 0.33324703097454900, 0.33274078072682400],
        [0.33391579279008200, 0.33325934921060100, 0.33282085708148900],
        [0.33381845494636700, 0.33327505027938300, 0.33290173128344400],
        [0.33367277492845600, 0.33329432844873200, 0.33302596748863200],
        [0.33356951340559100, 0.33330942495777500, 0.33311108308149700],
    ]
)

MSDS_BASIS_FUNCTIONS_sRGB_MALLETT2019: MultiSpectralDistributions = (
    MultiSpectralDistributions(
        DATA_BASIS_FUNCTIONS_sRGB_MALLETT2019,
        SPECTRAL_SHAPE_sRGB_MALLETT2019.wavelengths,
        name="Basis Functions - sRGB - Mallett 2019",
        labels=("red", "green", "blue"),
    )
)
"""
*Mallett and Yuksel (2019)* basis functions for the *sRGB* colourspace.

References
----------
:cite:`Mallett2019`
"""
