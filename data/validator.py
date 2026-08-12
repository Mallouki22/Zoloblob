"""
Data Validator

Vérifie la qualité des données historiques.
"""


class DataValidator:


    def __init__(self, df):

        self.df = df



    def check_empty(self):

        if self.df.empty:
            raise ValueError(
                "Dataset vide"
            )

        return True



    def check_missing(self):

        missing = self.df.isnull().sum()

        if missing.any():

            print(
                "⚠️ Valeurs manquantes :"
            )

            print(
                missing[missing > 0]
            )

            return False


        return True



    def check_duplicates(self):

        duplicates = (
            self.df
            .duplicated()
            .sum()
        )


        if duplicates > 0:

            print(
                f"⚠️ Doublons trouvés : {duplicates}"
            )

            return False


        return True



    def run(self):

        print("\n===== VALIDATION =====")


        results = {

            "empty":
            self.check_empty(),

            "missing":
            self.check_missing(),

            "duplicates":
            self.check_duplicates()

        }


        print(results)


        return all(results.values())