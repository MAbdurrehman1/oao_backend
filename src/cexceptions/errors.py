UNIQUE_ARGUMENT_ERROR = "{arg} ({value}) already exists."
INVALID_ARGUMENT_ERROR = "({values}) is/are not valid value for {entities}."
NOT_FOUND_ENTITY_ERROR = "{entity} with {arg} ({value}) not found."
INVALID_CREDENTIALS_ERROR = "{entity} is invalid."
EXPIRE_ERROR = "{entity} is no longer valid."
EXTERNAL_SOURCE_ERROR = "{source} failed with message: ({source_error})"
MISSING_ENTITY_ERROR = "{entity} must be provided."
MISSING_VALUES_ERROR = "{values} is/are missing in {entities}."
UNAUTHORIZED_ERROR = "user is not authorized to visit the content."
ENTITY_PROCESS_ERROR = "Failed to process {entity}. please provide a valid {entity}"
LESS_OR_EQUAL_ERROR = "{first_entity} must be less than or equal to {second_entity}"
GREATER_OR_EQUAL_ERROR = (
    "{first_entity} must be greater than or equal to {second_entity}"
)
DOES_NOT_BELONG_ERROR = (
    "{first_entity} ({first_value}) does not belong "
    "to this {second_entity} ({second_value})"
)
EMPTY_RESULT_ERROR = "No {first_entity} found for {second_entity}"
ALREADY_BELONG_ERROR = (
    "{owned_entity} with {arg}('s)" " {values} already belong to a {owner_entity}"
)
UNIQUE_PER_ENTITY_ARGUMENT_ERROR = "{first_entity} should be unique by {second_entity}"
