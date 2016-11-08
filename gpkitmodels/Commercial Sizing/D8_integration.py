"""temporary file containing classes in flux for full aircraft integration"""
from numpy import pi, tan, cos
import numpy as np
from gpkit import Variable, Model, units, SignomialsEnabled
from gpkit.constraints.sigeq import SignomialEqualityConstraint as SignomialEquality
from gpkit.constraints.tight import TightConstraintSet as TCS

class Engine(Model):
    """
    place holder engine model
    """
    def __init__(self, **kwargs):
        #new variables
        W_engine = Variable('W_{engine}', 'N', 'Weight of a Single Turbofan Engine')
        A2 = Variable('A_2', 'm^2', 'Fan Area')
        
        constraints = []

        constraints.extend([
            W_engine == 1000 * units('N'),

            A2 == A2,
            ])

        Model.__init__(self, None, constraints)

    def dynamic(self, state):
            """
            returns an engine performance model
            """
            return EnginePerformance(self, state)

class EnginePerformance(Model):
    """
    place holder engine perofrmacne model
    """
    def __init__(self, engine, state, **kwargs):
        #new variables
        TSFC = Variable('TSFC', '1/hr', 'Thrust Specific Fuel Consumption')
        thrust = Variable('thrust', 'N', 'Thrust')
        
        #constraints
        constraints = []

        constraints.extend([
            TSFC == TSFC,

            thrust == thrust, #want thrust to enter the model
            ])

        Model.__init__(self, None, constraints)


class Fuselage(Model):
    """
    place holder fuselage model
    """
    def __init__(self, **kwargs):
        #new variables
        n_pax = Variable('n_{pax}', '-', 'Number of Passengers to Carry')
                           
        #weight variables
        W_payload = Variable('W_{payload}', 'N', 'Aircraft Payload Weight')
        W_e = Variable('W_{e}', 'N', 'Empty Weight of Aircraft')
        W_pax = Variable('W_{pax}', 'N', 'Estimated Average Passenger Weight, Includes Baggage')

        A_fuse = Variable('A_{fuse}', 'm^2', 'Estimated Fuselage Area')
        pax_area = Variable('pax_{area}', 'm^2', 'Estimated Fuselage Area per Passenger')

        lfuse   = Variable('l_{fuse}', 'm', 'Fuselage length')
        xCG    = Variable('x_{CG}', 'm', 'x-location of CG')

        constraints = []
        
        constraints.extend([
            #compute fuselage area for drag approximation
            A_fuse == pax_area * n_pax,

            #constraints on the various weights
            W_payload == n_pax * W_pax,
            
            #estimate based on TASOPT 737 model
            W_e == .75*W_payload,

            lfuse == lfuse,
            xCG == xCG,
            ])

        Model.__init__(self, None, constraints)

    def dynamic(self, state):
        """
        returns a fuselage performance model
        """
        return FuselagePerformance(self, state)

class FuselagePerformance(Model):
    """
    Fuselage performance model
    """
    def __init__(self, fuse, state, **kwargs):
        #new variables
        Cdfuse = Variable('C_{D_{fuse}}', '-', 'Fuselage Drag Coefficient')
        Dfuse = Variable('D_{fuse}', 'N', 'Total Fuselage Drag')
        
        #constraints
        constraints = []

        constraints.extend([
            Dfuse == Cdfuse * (.5 * fuse['A_{fuse}'] * state.atm['\\rho'] * state['V']**2),

            Cdfuse == .005,
            ])

        Model.__init__(self, None, constraints)