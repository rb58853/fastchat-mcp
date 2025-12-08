def service2args(query: str, service: dict):
    return "{" + f'"User Query": {query}, "Service":{service}' + "}"
    # return f'{query}.\n Use the following service as information base:\n{service}'


# def query_and_services(query: str, services: str | list):
#     return "{" + f'"User Query": {query}, "All Services":{services}' + "}"
    # return f"{query}.\n The available services for obtaining information are:\n{services}"


def exposed_prompts(prompt_services: str | list):
    return (
        f"All prompt services:{prompt_services}"
        if len(prompt_services) > 0
        else "There are not prompts aviables. Your respose should be `[]`."
    )


# def query_and_data(query: str, data: str | dict):
#     return f"""{query}.\n Use the following retrieved data to answer my query. Assume that this data is complete, correct, and represents absolute truth. Do not question, reinterpret, or attempt to validate it; base your entire answer solely on this data as factually accurate and authoritative:\n{data}"""

#     # return f"{query}.\n Use the following retrieved data to answer my query:\n{data}"
