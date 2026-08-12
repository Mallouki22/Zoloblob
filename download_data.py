from data.downloader import DataDownloader
from data.validator import DataValidator

def main():

    downloader = DataDownloader()


    try:

        df = downloader.download()
        validator = DataValidator(df)

        validator.run()

        print("\n===== DATA =====")
        print(df.head())

        print("\nNombre de lignes :")
        print(len(df))


        downloader.save(df)


    finally:

        downloader.client.shutdown()



if __name__ == "__main__":
    main()