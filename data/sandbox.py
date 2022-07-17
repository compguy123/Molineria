from data.unit_of_work import MolineriaUnitOfWork


with MolineriaUnitOfWork("data/molineria.db") as uow:
    uow: MolineriaUnitOfWork
    # try it out