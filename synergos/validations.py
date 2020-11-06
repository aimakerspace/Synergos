#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging
from typing import Dict, List

# Libs


# Custom
from .base import BaseTask
from .endpoints import VALIDATION_ENDPOINTS

##################
# Configurations #
##################


##########################################
# Validation task Class - ValidationTask #
##########################################

class ValidationTask(BaseTask):
    """ Interfacing class governing all validation-related interactions with 
        the remote Synergos grid.

        Note: 
        This is a phase 3 process (i.e. evaluation), meaning that unlike those 
        in phase 1 (i.e. connection), the objective is to trigger a remote 
        process. Also, outputs are dependent on the models obtained during phase
        2 (i.e. training). Hence, options to update or delete attributes are 
        removed, since the system detects and adapts to base configurations 
        dynamically.
        

    Attributes:
        _type (str): Specifies the type of task
        address (str): Address where Synergos TTP is hosted at
        endpoints (str)): All endpoints governed by this task
    """

    def __init__(self, address: str):
        super().__init__(
            _type="validation", 
            address=address,
            endpoints=VALIDATION_ENDPOINTS
        )
        
    ###########
    # Helpers #
    ###########

    def _generate_url(
        self, 
        project_id: str, 
        expt_id: str = None,
        run_id: str = None,
        participant_id: str = None
    ) -> str:
        if project_id and expt_id and run_id and participant_id:
            return super()._generate_url(
                endpoint=self.endpoints.PARTICIPANT_COMBINATION,
                project_id=project_id,
                expt_id=expt_id,
                run_id=run_id,
                participant_id=participant_id
            )

        elif project_id and expt_id and run_id:
            return super()._generate_url(
                endpoint=self.endpoints.RUN_COMBINATIONS,
                project_id=project_id,
                expt_id=expt_id,
                run_id=run_id
            )

        elif project_id and expt_id:
            return super()._generate_url(
                endpoint=self.endpoints.EXPERIMENT_COMBINATIONS,
                project_id=project_id,
                expt_id=expt_id
            )

        elif project_id:
            return super()._generate_url(
                endpoint=self.endpoints.PROJECT_COMBINATIONS,
                project_id=project_id
            )

        else:
            raise ValueError("Validation triggers are restricted to the project scope. Specify at least 1 project!")

    ##################
    # Core functions #
    ##################

    def create(
        self, 
        project_id: str, 
        expt_id: str = None,
        run_id: str = None,
        participant_id: str = None,
        auto_align: bool = True,
        dockerised: bool = True,
        verbose: bool = True,
        log_msgs: bool = True,
        **kwargs
    ):
        """ Triggers multiple feature alignment for the participant under a 
            specific project in the federated grid

        Args:
            project_id (str): Identifier of project
            expt_id (str): Identifier of experiment run is under
            run_id (str): Identifier of run
            participant_id (str): Identifier of participant
            auto_align (bool): Toggles if multiple feature alignments will be used
            dockerised (bool): Toggles if orchestrations are dockerised
            log_msgs (bool): Toggles if computation operations should be logged
            verbose (bool): Toggles verbosity of computation logging
            **kwargs
        Returns:
            
        """
        parameters = {
            "auto_align": auto_align,
            "dockerised": dockerised,
            "verbose": verbose,
            "log_msgs": log_msgs
        }

        return self._execute_operation(
            operation="post",
            url=self._generate_url(
                project_id=project_id,
                expt_id=expt_id,
                run_id=run_id,
                participant_id=participant_id
            ),
            payload=parameters
        )


    def read(
        self, 
        project_id: str, 
        expt_id: str = None,
        run_id: str = None,
        participant_id: str = None
    ):
        """ Retrieves a single set of tags' information/configurations created
            in the federated grid

        Args:
            project_id (str): Identifier of project
            expt_id (str): Identifier of experiment run is under
            run_id (str): Identifier of run
            participant_id (str): Identifier of participant
        Returns:

        """
        return self._execute_operation(
            operation="get",
            url=self._generate_url(
                project_id=project_id,
                expt_id=expt_id,
                run_id=run_id,
                participant_id=participant_id
            ),
            payload=None
        )
    

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    address = f"http://{host}:{port}"

    from .projects import ProjectTask
    from .experiments import ExperimentTask
    from .runs import RunTask
    from .participants import ParticipantTask
    from .registrations import RegistrationTask
    from .tags import TagTask
    from .alignments import AlignmentTask
    from .models import ModelTask
    
    # Create reference project
    projects = ProjectTask(address)
    project_id = "test_project"
    projects.create(
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
        'criterion': "NLLLoss", 
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
        project_id=project_id,
        expt_id=expt_id_1,
        run_id=run_id_1,
        **parameter_set_1
    )

    runs.create( # Use default parameter set on model 1
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

    parameter_set_1 = {
        'host': '172.17.0.2',
        'port': 8020,
        'f_port': 5000,
        'log_msgs': True,
        'verbose': True
    }
    participants.create(participant_id=participant_id_1, **parameter_set_1)

    parameter_set_2 = {
        'host': '172.17.0.3',
        'port': 8020,
        'f_port': 5000,
        'log_msgs': True,
        'verbose': True
    }
    participants.create(participant_id=participant_id_2, **parameter_set_2)  

    # Create reference registrations
    registrations = RegistrationTask(address)
    registrations.create(
        project_id=project_id,
        participant_id=participant_id_1,
        role='host'
    )

    registrations.create(
        project_id=project_id,
        participant_id=participant_id_2,
        role='guest'
    )

    # Create reference tags
    tags = TagTask(address)
    tags.create(
        project_id=project_id,
        participant_id=participant_id_1,
        train=[
            # ["non_iid_1"], 
            # ["edge_test_missing_coecerable_vals"],
            ["edge_test_misalign"],
            ["edge_test_na_slices"]
        ],
        evaluate=[["iid_1"]]
    )

    tags.create(
        project_id=project_id,
        participant_id=participant_id_2,
        train=[["non_iid_2"]]
    )

    # Create reference alignments
    alignments = AlignmentTask(address)
    create_response = alignments.create(project_id=project_id)

    # Create reference models
    models = ModelTask(address)
    models.create( # All combinations under a project
        project_id=project_id
    )

    validations = ValidationTask(address)

    # Test validation(s) creation
    create_response_1 = validations.create( # A single participant combination
        project_id=project_id,
        expt_id=expt_id_2,
        run_id=run_id_2,
        participant_id=participant_id_1
    )
    print("Validations: Create response 1:", create_response_1)

    create_response_2 = validations.create( # All combinations under a run
        project_id=project_id,
        expt_id=expt_id_2,
        run_id=run_id_2
    )
    print("Validations: Create response 2:", create_response_2)

    create_response_3 = validations.create( # All combinations under an expt
        project_id=project_id,
        expt_id=expt_id_1
    )
    print("Validations: Create response 3:", create_response_3)

    create_response_4 = validations.create( # All combinations under a project
        project_id=project_id
    )
    print("Validations: Create response 4:", create_response_4)

    # Test validation(s) retrieval
    read_response_1 = validations.read( # A single participant combination
        project_id=project_id,
        expt_id=expt_id_2,
        run_id=run_id_2,
        participant_id=participant_id_1
    )
    print("Validations: Read response 1:", read_response_1)

    read_response_2 = validations.read( # All combinations under a run
        project_id=project_id,
        expt_id=expt_id_2,
        run_id=run_id_2
    )
    print("Validations: Read response 2:", read_response_2)

    read_response_3 = validations.read( # All combinations under an expt
        project_id=project_id,
        expt_id=expt_id_1
    )
    print("Validations: Read response 3:", read_response_3)

    read_response_4 = validations.read( # All combinations under a project
        project_id=project_id
    )
    print("Validations: Read response 4:", read_response_4)

    # Clean up
    projects.delete(project_id=project_id)