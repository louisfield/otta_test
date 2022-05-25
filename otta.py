import itertools
import typing

import pandas as pd
from pandas.core.frame import DataFrame


def _setup_companies() -> DataFrame:
    # Reads jobs.csv file
    return pd.read_csv('./data/jobs.csv')


def _setup_reactions() -> DataFrame:
    # Reads reactions.csv file
    reactions = pd.read_csv('./data/reactions.csv')
    reactions = reactions[reactions.direction == True]
    return reactions


def _setup_user_reactions(
    reactions: DataFrame,
    field_one: str,
    field_two: str,
) -> dict[int, typing.Set[int]]:
    """
    Generates a dictionary from a DataFrame which stores 
    the field_two parameter grouped by the field_two parameter
    """
    reactions = reactions.groupby(field_one)[field_two]

    reactions = reactions.apply(list)

    ids_one = reactions.keys()
    ids_two = [set(x) for x in reactions.values]

    return dict(zip(ids_one, ids_two))


def _setup_company_jobs(
    companies: DataFrame,
) -> dict[int, typing.Set[int]]:
    """
    Generates a dictionary from a DataFrame which stores 
    job ids grouped by company ids
    """
    companies = companies.groupby('company_id')['job_id']
    companies = companies.apply(list)
    company_ids = companies.keys()

    job_ids = [frozenset(x) for x in companies.values]

    company_ids = dict(zip(company_ids, job_ids))

    return company_ids


def _calculate_similarity(ids: dict[int, typing.Set[int]]) -> None:
    """
    Calculates highest similarity value between users 
    which is the highest amount of jobs liked between 
    two users
    """
    similarity = 0
    id_1 = ''
    id_2 = ''

    for a, b in itertools.combinations(ids.keys(), 2):
        intersection = len(ids[a].intersection(ids[b]))
        if intersection > similarity:
            similarity = intersection
            id_1 = a
            id_2 = b

    print('Similarity is: {}, and the ids are {} and {}'.format(
        similarity, id_1, id_2))


def _calculate_company_similarity(
    reaction_ids: dict[int, typing.Set[int]], 
    company_ids: dict[int, typing.Set[int]]
) -> None:
    """
    Calculates highest similarity value between companies 
    which is the highest amount of users that like at least
    one job at both companies
    """
    similarity = 0
    id_1 = ''
    id_2 = ''

    for a, b in itertools.combinations(company_ids.keys(), 2):
        jobs_a = company_ids.get(a)
        jobs_b = company_ids.get(b)

        users_a = set().union(*[reaction_ids.get(x)
                                for x in jobs_a if reaction_ids.get(x)])
        users_b = set().union(*[reaction_ids.get(x)
                                for x in jobs_b if reaction_ids.get(x)])

        intersection = len(users_a.intersection(users_b))
        if intersection > similarity:
            similarity = intersection
            id_1 = a
            id_2 = b

    print('Similarity is: {}, and the ids are {} and {}'.format(
        similarity, id_1, id_2))


def main():
    reactions = _setup_reactions()

    reaction_ids = _setup_user_reactions(reactions, 'user_id', 'job_id')
    _calculate_similarity(reaction_ids)

    companies = _setup_companies()
    reaction_ids = _setup_user_reactions(reactions, 'job_id', 'user_id')
    company_ids = _setup_company_jobs(companies)
    _calculate_company_similarity(reaction_ids, company_ids)


if __name__ == "__main__":
    main()
