import requests
import zipfile
import os
import json


class WiderFaceTest:
    """Test images importing"""

    URL = "https://drive.google.com/uc?export=download&"
    ID = "183a2_aLUGftx8b4M1PELUYN1k-P-bh4M"
    FNAME = 'WiderFaces.zip'

    def get_confirm_token(self, response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def download_files(self):
        """Downloading test images and description for these images"""

        if os.path.isdir("WiderFacesTest/"):
            print("Dir exists.")
        else:
            session = requests.Session()

            response = session.get(self.URL, params={'id': self.ID}, stream=True)
            token = self.get_confirm_token(response)

            if token:
                params = {'id': id, 'confirm': token}
                response = session.get(self.URL, params=params, stream=True)

            CHUNK_SIZE = 32768

            with open(self.FNAME, "wb") as f:
                for chunk in response.iter_content(CHUNK_SIZE):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)

            with zipfile.ZipFile(self.FNAME, "r") as zip_ref:
                zip_ref.extractall()
            os.remove("WiderFaces.zip")

    def test_generate(self):
        """Image Description Generator"""
        with open("WiderFacesTest/WiderFacesTest.json") as json_file:
            wft_anot = json.load(json_file)
            for key in wft_anot:
                record = {
                    "image_name": key,
                    'count': wft_anot[key]['face_count'],
                    "path": wft_anot[key]['folder'],
                    'bboxes': wft_anot[key]['bboxes'],
                }
                yield record


if __name__ == "__main__":
    WFT = WiderFaceTest()
    WFT.download_files()







