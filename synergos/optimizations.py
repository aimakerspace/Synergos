#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging
from typing import Dict, List, Union

# Libs


# Custom
from .base import BaseTask
from .endpoints import OPTIMIZATION_ENDPOINTS

##################
# Configurations #
##################


##############################################
# Optimization task Class - OptimizationTask #
##############################################

class OptimizationTask(BaseTask):
    """ Interfacing class governing all optimization-related interactions with 
        the remote Synergos grid.

        Note: 
        This is a phase 2 process (i.e. training), meaning that unlike those in 
        phase 1 (i.e. connection), the objective is to trigger a remote process.
        Hence, options to update or delete attributes are removed, since the
        system detects and adapts to base configurations dynamically.
        

    Attributes:
        _type (str): Specifies the type of task
        address (str): Address where Synergos TTP is hosted at
        endpoints (str)): All endpoints governed by this task
    """

    def __init__(self, address: str):
        super().__init__(
            _type="optimization", 
            address=address,
            endpoints=OPTIMIZATION_ENDPOINTS
        )
        
    ###########
    # Helpers #
    ###########

    def _generate_url(
        self, 
        collab_id: str, 
        project_id: str, 
        expt_id: str
    ) -> str:
        return super()._generate_url(
            endpoint=self.endpoints.OPTIMIZATIONS,
            collab_id=collab_id,
            project_id=project_id,
            expt_id=expt_id
        )

    ##################
    # Core functions #
    ##################


    def create(
        self, 
        collab_id: str,
        project_id: str,
        expt_id: str,
        search_space: Dict[str, Dict[str, Union[str, bool, int, float]]],
        # tuner: str,
        metric: str,
        optimize_mode: str,
        trial_concurrency: int = 1,
        max_exec_duration: str = "1h",
        max_trial_num: int = 10,
        is_remote: bool = True,
        use_annotation: bool = True,
        auto_align: bool = True,
        dockerised: bool = True,
        verbose: bool = True,
        log_msgs: bool = True,
        **kwargs
    ):
        """ Triggers multiple feature alignment for the participant under a 
            specific project in the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
            expt_id (str): Identifier of experiment run is under
            run_id (str): Identifier of run
            dockerised (bool): Toggles if orchestrations are dockerised
            log_msgs (bool): Toggles if computation operations should be logged
            verbose (bool): Toggles verbosity of computation logging
            **kwargs
        Returns:
            
        """
        parameters = {
            'search_space': search_space,
            # 'tuner': tuner,
            'metric': metric,
            'optimize_mode': optimize_mode,
            'trial_concurrency': trial_concurrency,
            'max_exec_duration': max_exec_duration,
            'max_trial_num': max_trial_num,
            'is_remote': is_remote,
            'use_annotation': use_annotation,
            'auto_align': auto_align,
            'dockerised': dockerised,
            'verbose': verbose,
            'log_msgs': log_msgs,
            **kwargs
        }

        return self._execute_operation(
            operation="post",
            url=self._generate_url(
                collab_id=collab_id,
                project_id=project_id,
                expt_id=expt_id
            ),
            payload=parameters
        )


    def read(self, collab_id: str, project_id: str, expt_id: str):
        """ Retrieves a single set of tags' information/configurations created
            in the federated grid

        Args:
            collab_id (str): Identifier of collaboration
            project_id (str): Identifier of project
            expt_id (str): Identifier of experiment run is under
            run_id (str): Identifier of run
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_url(
                collab_id=collab_id,
                project_id=project_id,
                expt_id=expt_id
            ),
            payload=None
        )
    

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    address = f"http://{host}:{port}"

    from .collaborations import CollaborationTask
    from .projects import ProjectTask
    from .experiments import ExperimentTask
    from .runs import RunTask
    from .participants import ParticipantTask
    from .registrations import RegistrationTask
    from .tags import TagTask
    from .alignments import AlignmentTask
    from .models import ModelTask
    from .validations import ValidationTask
    from .predictions import PredictionTask
    
    # Create a reference collaboration
    collaborations = CollaborationTask(address)
    collab_id = "test_collab"
    collaborations.create(collab_id=collab_id)

    # Create reference project
    projects = ProjectTask(address)
    project_id = "test_project"
    projects.create(
        collab_id=collab_id,
        project_id=project_id, 
        action="classify",
        incentives={
            'tier_1': [],
            'tier_2': []
        }
    )

    # Create reference experiments
    experiments = ExperimentTask(address)
    expt_id_1 = "test_expt_1"
    expt_id_2 = "test_expt_2"

    experiments.create(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_1,
        model=[
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 15,
                    "out_features": 1
                }
            }
        ]
    )

    experiments.create(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_2,
        model=[
            {
                "activation": "sigmoid",
                "is_input": True,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 30,
                    "out_features": 20
                }
            },
            {
                "activation": "sigmoid",
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 20,
                    "out_features": 10
                }
            },
            {
                "activation": "sigmoid",
                "is_input": False,
                "l_type": "Linear",
                "structure": {
                    "bias": True,
                    "in_features": 10,
                    "out_features": 1
                }
            }
        ]
    ) 

    # Create reference runs
    runs = RunTask(address)
    run_id_1 = "test_run_1"
    run_id_2 = "test_run_2"

    parameter_set_1 = {
        'algorithm': "FedProx", 
        'batch_size': 32, 
        'rounds': 2, 
        'epochs': 1,
        'lr': 0.001, 
        'weight_decay': 0.001,
        'lr_decay': 0.001, 
        'mu': 0.001, 
        'l1_lambda': 0.001, 
        'l2_lambda': 0.001,
        'optimizer': "SGD", 
        'criterion': "MSELoss", 
        'lr_scheduler': "CyclicLR", 
        'delta': 0.001,
        'patience': 10,
        'seed': 100,
        'is_snn': False, 
        'precision_fractional': 7,
        'base_lr': 0.0001,
        'max_lr': 0.001
    }
    runs.create(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_1,
        run_id=run_id_1,
        **parameter_set_1
    )

    runs.create( # Use default parameter set on model 1
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_1,
        run_id=run_id_2,
        rounds=2, 
        epochs=1,
        base_lr=0.0005,
        max_lr=0.005,
        criterion="NLLLoss"
    ) 

    runs.create( # Use default parameter set on model 2
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_2,
        run_id=run_id_2,
        rounds=2, 
        epochs=1,
        base_lr=0.0005,
        max_lr=0.005,
        criterion="NLLLoss"
    ) 

    # Create reference participants
    participants = ParticipantTask(address)
    participant_id_1 = "test_participant_1"
    participant_id_2 = "test_participant_2"

    parameter_set_1 = {}
    participants.create(participant_id=participant_id_1, **parameter_set_1)

    parameter_set_2 = {}
    participants.create(participant_id=participant_id_2, **parameter_set_2)  

    # Create reference registrations
    registrations = RegistrationTask(address)
    
    registrations.add_node(**{
        'host': '172.17.0.2',
        'port': 8020,
        'f_port': 5000,
        'log_msgs': True,
        'verbose': True
    })
    registrations.create(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_1,
        role='host'
    )

    registrations.add_node(**{
        'host': '172.17.0.3',
        'port': 8020,
        'f_port': 5000,
        'log_msgs': True,
        'verbose': True
    })
    registrations.create(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_2,
        role='guest'
    )

    # Create reference tags
    tags = TagTask(address)
    tags.create(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_1,
        train=[["tabular", "abalone", "data1", "train"]],
        evaluate=[["tabular", "abalone", "data1", "evaluate"]]
    )

    tags.create(
        collab_id=collab_id,
        project_id=project_id,
        participant_id=participant_id_2,
        train=[["tabular", "abalone", "data2", "train"]],
        evaluate=[["tabular", "abalone", "data2", "evaluate"]]
    )

    # Create reference alignments
    alignments = AlignmentTask(address)
    alignments.create(collab_id=collab_id, project_id=project_id)

    # # Create reference model(s)
    # models = ModelTask(address)
    # models.create( # All combinations under a project
    #     collab_id=collab_id,
    #     project_id=project_id,
    #     expt_id=expt_id_1,
    #     run_id=run_id_1
    # )

    optimizations = OptimizationTask(address)

    # Test optimization creation
    optim_parameters = {
        'search_space': {
            "rounds": {"_type":"choice","_value":[1, 2]},
            "epochs": {"_type":"choice","_value":[1, 2]},
            "batch_size": {"_type":"choice", "_value": [450, 512]},
            "lr":{"_type":"choice","_value":[0.0001, 0.1]},
            "criterion":{"_type":"choice","_value":["NLLLoss"]},
            "mu":{"_type":"uniform","_value":[0.0, 1.0]},
            "base_lr":{"_type":"choice","_value":[0.00005]},
            "max_lr":{"_type":"choice","_value":[0.2]}
        },
        'backend': "tune",
        'scheduler': "ASHAScheduler",
        'searcher': "TuneBOHB",
        'optimize_mode': "max",
        'metric': "accuracy",
        'trial_concurrency': 1,
        'max_exec_duration': "1h",
        'max_trial_num': 10,
        'max_concurrent': 1,
        'is_remote': True,
        'use_annotation': True,
        'auto_align': True,
        'dockerised': True,
        'verbose': True,
        'log_msgs': True
    }
    create_response = optimizations.create(
        collab_id=collab_id,
        project_id=project_id,
        expt_id=expt_id_1,
        **optim_parameters
    )
    print(f"Optimization: Create response: {create_response}")

    # Test optimization creation
    read_response = optimizations.read(
        collab_id=collab_id,
        project_id=project_id, 
        expt_id=expt_id_1
    )
    print(f"Optimization: Read response: {read_response}")

    # Clean up
    collaborations.delete(collab_id=collab_id)