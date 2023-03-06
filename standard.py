# -*- coding: utf-8 -*-
"""
Library of some standard materials

@author: Rouchier
"""

from hamopy.classes import Material

################
### Concrete ###
################

concrete = Material('concrete', rho = 2450., cp = 880.)

concrete.set_conduc(lambda_0=1.75,  lambda_m=4.5)
                 
concrete.set_isotherm('vangenuchten',**{"w_sat" : 101.44,
                                        "l"     : 1.,
                                        "alpha" : 6.165e-7,
                                        "m"     : 0.219 })
                                      
concrete.set_perm_vapor('schirmer',**{"mu" : 30.,
                                      "p"  : 0.497 } )
                                    
concrete.set_perm_liquid('durner', **{"K_sat" : 2.2182e-13,
                                      "tau"   : -4.6974,
                                      "l"     : [0.5062, 0.4938],
                                      "alpha" : [5.5383e-7, 2.2493e-8],
                                      "m"     : [0.6148, 0.1913] } )

#############################                       
### Wood fibre insulation ###
#############################

wood_fibre = Material('wood_fibre', rho= 146., cp = 1103.1)

wood_fibre.set_capacity(cp_0 = 1103.1, cp_t=11.271)

wood_fibre.set_conduc(lambda_0 = 0.038,
                      lambda_m = 0.192,
                      lambda_t = 0.108e-3)
"""                        
wood_fibre.set_isotherm('polynomial', **{"HR" : [0, 0.25, 0.5, 0.75],
                                         "W"  : [0, 6.981, 11.133, 19.299] })
wood_fibre.set_isotherm('slope', **{"HR" : [0.4, 0.6, 0.8],
                                    "XI" : [15.841, 28.686, 59.049] })
"""
wood_fibre.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                                    "XI" : [17.704, 20.074, 49.816] })


wood_fibre.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],
                                       "dp" : [3.75e-11, 6.59e-11] } )

wood_fibre.set_perm_air(4.16e-13)
#############################
### Steel ###
#############################

steel = Material('steel', rho= 7850., cp = 420.)

steel.set_capacity(cp_0= 420.,  cp_t = 1.)

steel.set_conduc(lambda_0= 45.,
                      lambda_m= 0.,
                      lambda_t= 0.)
"""                        
wood_fibre.set_isotherm('polynomial', **{"HR" : [0, 0.25, 0.5, 0.75],
                                         "W"  : [0, 6.981, 11.133, 19.299] })
wood_fibre.set_isotherm('slope', **{"HR" : [0.4, 0.6, 0.8],
                                    "XI" : [15.841, 28.686, 59.049] })
"""
steel.set_isotherm('slope', **{"HR": [0.25, 0.5, 0.75],
                                    "XI": [1.0e-16, 1.0e-15, 5.0e-15]})


steel.set_perm_vapor('interp', **{"HR": [0.25, 0.75],
                                       "dp": [1.0e-15, 1.0e-15]})

steel.set_perm_air(1.0e-16)
#############################
### Wood ###
#############################
wood = Material('wood', rho = 450., cp = 1760.)

wood.set_capacity(cp_0 = 1760.,  cp_t = 1.)

wood.set_conduc(lambda_0 = 0.072,
                      lambda_m = 0.,
                      lambda_t = 0.)
"""                        
wood_fibre.set_isotherm('polynomial', **{"HR" : [0, 0.25, 0.5, 0.75],
                                         "W"  : [0, 6.981, 11.133, 19.299] })
wood_fibre.set_isotherm('slope', **{"HR" : [0.4, 0.6, 0.8],
                                    "XI" : [15.841, 28.686, 59.049] })
"""
wood.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75], #  10.1088/1742-6596/2069/1/012009
                                    "XI" : [8., 10., 16.] })


wood.set_perm_vapor('interp', **{"HR" : [0.25, 0.75],      #
                                       "dp" : [1.0e-10, 1.0e-10] } ) # http://dx.doi.org/10.4067/S0718-221X2015005000002
wood.set_perm_air(1.0e-13)
#############################
#
# materials in STATICUS
#
#############################
### Spruce ###
#############################
spruce = Material('spruce', rho = 390., cp = 1600.)

spruce.set_capacity(cp_0=1600., cp_t=1.)

spruce.set_conduc(lambda_0=0.128,      # lambda = lambda_0 + w(kg/m3)/1000 * lambda_m + T(°C) * lambda_t
                      lambda_m=320.,      # WUFI
                      lambda_t=0.0002)
spruce.set_isotherm('polynomial', **{"HR": [0.0, 0.4, 0.8, 0.95],  #  WUFI
                                    "W": [0.0, 30., 60., 75.]})
spruce.set_perm_vapor('interp', **{"HR": [0.0, 0.3, 0.4, 0.6, 0.7, 1.0],      #
                                       "dp": [6.8e-11, 6.8e-11, 8.7e-11, 1.9e-10, 2.6e-10, 2.6e-10] } ) # WUFI
spruce.set_perm_air(0.0)   # file:///C:/Users/katarzynao/Downloads/767-Article%20Text-767-1-10-20141206.pdf
#############################
### glass ###
#############################
glass = Material('glass', rho=2500., cp=750.)

glass.set_capacity(cp_0=750., cp_t=1.)

glass.set_conduc(lambda_0=1.0,           # lambda = lambda_0 + w(kg/m3)/1000 * lambda_m + T(°C) * lambda_t
                      lambda_m=0.0,      # WUFI
                      lambda_t=0.0)
glass.set_isotherm('polynomial', **{"HR": [0.0, 0.4, 0.8, 0.95],    # WUFI
                                    "W": [0.0, 0.0005, 0.001, 0.002]})
glass.set_perm_vapor('interp', **{"HR": [0.0, 0.3, 0.4, 0.6, 0.7, 1.0],      #
                                    "dp": [6.8e-13, 6.8e-13, 8.7e-12, 1.9e-11, 2.6e-11, 2.6e-11]})   # WUFI 6.8e-13, 6.8e-13, 8.7e-13, 1.9e-11, 2.6e-11, 2.6e-11
glass.set_perm_air(1.0e-13)   # file:///C:/Users/katarzynao/Downloads/767-Article%20Text-767-1-10-20141206.pdf
#############################
### argon ###
#############################
argon = Material('argon', rho=1.7, cp=519.)

argon.set_capacity(cp_0=519., cp_t=1.)

argon.set_conduc(lambda_0=0.017,      # lambda = lambda_0 + w(kg/m3)/1000 * lambda_m + T(°C) * lambda_t
                      lambda_m=0.,      # WUFI
                      lambda_t=0.)
argon.set_isotherm('polynomial', **{"HR" : [0.0, 0.4, 0.6, 0.8],  #  WUFI
                                    "W" : [0.001, 0.4, 1.0, 2.0] })
argon.set_perm_vapor('interp', **{"HR" : [0.0, 0.3, 0.9],      #
                                       "dp" : [7.4e-9, 7.3e-9, 7.2e-9] } ) # WUFI diff res factor = 1   7.4e-9, 7.0e-9, 6.5e-9, 6.0e-9, 5.0e-9
argon.set_perm_air(1.0)   # ?
#############################
### MW_semi_hard ###
#############################
mw_sh = Material('mw_sh', rho=40.0, cp=1030.)

mw_sh.set_capacity(cp_0=1030., cp_t=1.)

mw_sh.set_conduc(lambda_0=0.029,      # lambda = lambda_0 + w(kg/m3)/1000 * lambda_m + T(°C) * lambda_t
                      lambda_m=45.,      # WUFI
                      lambda_t=0.0002)
#mw_sh.set_isotherm('slope', **{"HR" : [0.0, 0.5, 0.8],  #  WUFI
#                                    "XI" : [0.002, 0.002, 0.002] })
mw_sh.set_isotherm('polynomial', **{"HR": [0.0, 0.4, 0.6, 0.8],    # WUFI
                                    "W": [0.002, 0.002, 0.002, 0.002]})
mw_sh.set_perm_vapor('interp', **{"HR": [0.0, 0.3, 0.9],      #
                                       "dp" : [7.4e-9, 7.3e-9, 7.2e-9] } ) # WUFI diff res factor = 1
mw_sh.set_perm_air(1.0e-13)   # ??? to do
#############################
### MW_soft ###
#############################
mw_soft = Material('mw_soft', rho=25.2, cp=1000.)

mw_soft.set_capacity(cp_0=1000., cp_t=1.)

mw_soft.set_conduc(lambda_0=0.033,      # lambda = lambda_0 + w(kg/m3)/1000 * lambda_m + T(°C) * lambda_t
                      lambda_m=85.,      # WUFI
                      lambda_t=0.0002)
mw_soft.set_isotherm('polynomial', **{"HR": [0.0, 0.4, 0.9, 0.95],  #  WUFI
                                    "W" : [0.002, 0.002, 0.002, 0.002] })
mw_soft.set_perm_vapor('interp', **{"HR": [0.0, 0.8, 1.0],      #
                                       "dp" : [7.4e-9, 7.3e-9, 7.2e-9] } ) # WUFI diff res factor = 1
mw_soft.set_perm_air(1.0e-13)   # ??? to do
#############################
### ZINC ###
#############################
zinc = Material('zinc', rho=7200., cp=380.)

zinc.set_capacity(cp_0=380., cp_t=1.)

zinc.set_conduc(lambda_0=110.,      # lambda = lambda_0 + w(kg/m3)/1000 * lambda_m + T(°C) * lambda_t
                      lambda_m =0.,      # WUFI
                      lambda_t=0.)
#zinc.set_isotherm('polynomial', **{"HR": [0.0, 0.6, 0.8, 0.9],  #  WUFI
#                                    "W": [0.0, 0.0001, 0.0002, 0.005]})
zinc.set_isotherm('slope', **{"HR": [0.25, 0.5, 0.75],
                                    "XI" : [1.0e-16, 1.0e-15, 5.0e-15] })
#zinc.set_perm_vapor('interp', **{"HR": [0.0, 1.0],      #
#                                       "dp": [1.8e-12, 1.0e-12] } ) # WUFI diff res factor mu= 0.0001 ????!!!!!
zinc.set_perm_vapor('interp', **{"HR": [0.25, 0.75],
                                       "dp": [1.0e-15, 1.0e-15]})
zinc.set_perm_air(1.0e-16)   # ??? to do
#############################
### ALUMINIUM ###
#############################
aluminium = Material('aluminium', rho=2700., cp=900.)

aluminium.set_capacity(cp_0=900., cp_t=1.)

aluminium.set_conduc(lambda_0=200.,      # lambda = lambda_0 + w(kg/m3)/1000 * lambda_m + T(°C) * lambda_t
                      lambda_m=0.,      # WUFI
                      lambda_t=0.)
#aluminium.set_isotherm('polynomial', **{"HR" : [0.0, 0.6, 0.8, 0.9],  #  WUFI
#                                    "W" : [0.0, 0.001, 0.002, 0.005] })
aluminium.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                                    "XI" : [1.0e-16, 1.0e-15, 5.0e-15] })
aluminium.set_perm_vapor('interp', **{"HR" : [0.0, 1.0],      #
                                       "dp" : [1.8e-12, 1.0e-12] } ) # WUFI diff res factor mu= 0.0001 ????!!!!!
aluminium.set_perm_air(1.0e-13)   # ??? to do
#############################
### GLUE ###
#############################
glue = Material('glue', rho=1200., cp=1800.)

glue.set_capacity(cp_0=1800., cp_t=1.)

glue.set_conduc(lambda_0=0.24,      # lambda = lambda_0 + w(kg/m3)/1000 * lambda_m + T(°C) * lambda_t
                      lambda_m=0.,      # WUFI
                      lambda_t=0.001)
#glue.set_isotherm('polynomial', **{"HR" : [0.0, 0.6, 0.8, 0.9],  #  WUFI
#                                    "W" : [0.0, 0.001, 0.002, 0.005] })
glue.set_isotherm('slope', **{"HR" : [0.25, 0.5, 0.75],
                                    "XI" : [1.0e-16, 1.0e-15, 5.0e-15] })
glue.set_perm_vapor('interp', **{"HR" : [0.0, 1.0],      #
                                       "dp" : [1.2e-12, 1.2e-12] } ) # WUFI mu = 6000
glue.set_perm_air(1.0e-13)   # ??? to do
#############################
### polyiso_ins ###
#############################
polyiso_ins = Material('polyiso_ins', rho=32.5, cp=1470.)

polyiso_ins.set_capacity(cp_0=1470., cp_t=1.)

polyiso_ins.set_conduc(lambda_0=0.022,      # lambda = lambda_0 + w(kg/m3)/1000 * lambda_m + T(°C) * lambda_t
                      lambda_m=657.5,      # WUFI
                      lambda_t=0.0002)
polyiso_ins.set_isotherm('polynomial', **{"HR" : [0.0, 0.4, 0.8, 0.9],  #  WUFI
                                    "W" : [0.0, 0.5, 1.2, 1.6] })
polyiso_ins.set_perm_vapor('interp', **{"HR" : [0.0, 0.8, 0.9, 1.0],      #
                                       "dp" : [1.0e-10, 1.6e-10, 1.7e-10, 1.7e-10] } ) # WUFI mu = 72 down to 42
polyiso_ins.set_perm_air(1.0e-13)   # ??? to do
#############################