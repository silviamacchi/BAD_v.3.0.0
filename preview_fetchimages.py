import os
import requests
from qgis.PyQt import uic, QtWidgets
from qgis.PyQt.QtWidgets import QFileDialog, QGraphicsScene
from qgis.PyQt.QtGui import QImage, QPixmap, QColor
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'preview_fetchimages.ui'))

class PreviewFetchImages(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, bbox, date,  image_list, current_index, cloud, user=None, password=None, parent=None):
        super(PreviewFetchImages, self).__init__(parent)
        self.setupUi(self)
        
        self.preview_scene = QGraphicsScene()
        self.graphicsView.setScene(self.preview_scene)
        
        self.lineEdit.setVisible(False)

        self.image_list = image_list
        self.current_index = current_index
        date = self.image_list[self.current_index]

        self.leftButton.clicked.connect(lambda: self.go_left(bbox, date, cloud, user, password))
        self.rightButton.clicked.connect(lambda: self.go_right(bbox, date, cloud, user, password))



        self.pixmap = self.get_sentinel_preview(
            client_id=user,
            client_secret=password,
            bbox=bbox,
            date=date,
            cloud=cloud
            )

        self.radioButton_RGB.toggled.connect(lambda: self.update_preview(bbox, date, cloud, user, password))
        self.radioButton_NBR.toggled.connect(lambda: self.update_preview(bbox, date, cloud, user, password))

        if self.pixmap:
            self.draw_scene()
        else:
            self.lineEdit.setVisible(True)
            self.lineEdit.setStyleSheet("color: red; font-weight: bold;")
            print("Not possible to get the image.")
            self.leftButton.setEnabled(False)
            self.rightButton.setEnabled(False)
    
        self.btnClose.clicked.connect(self.close)

    def get_sentinel_preview(self, client_id, client_secret, bbox, date, cloud):

        # left right buttons
        if self.current_index == 0:
            self.leftButton.setEnabled(False)
            self.rightButton.setEnabled(True)
        elif self.current_index == len(self.image_list) - 1:
            self.rightButton.setEnabled(False)
            self.leftButton.setEnabled(True)
        else:
            self.leftButton.setEnabled(True)
            self.rightButton.setEnabled(True) 
        
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        if height:
            proportion=width/height
            if proportion>1:
                height=(512*height)/width
                width=512
            else:
                width=(512*width)/height
                height=512
        else:
            width = 512
            height = 512


        # display image date
        self.label_imageDate.setText(f"Image date: {date}")

        # Step 1: access token
        token_url = "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token"
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        token_response = requests.post(token_url, data=token_data)
        access_token = token_response.json().get("access_token")

        print("Token response:", token_response.status_code)
        print("Token body:", token_response.text)

        # Step 2: Request Process API
        process_url = f"https://sh.dataspace.copernicus.eu/api/v1/process"
        headers = {"Authorization": f"Bearer {access_token}"}

        payload = {}

        if self.radioButton_RGB.isChecked():
            payload = {
                "input": {
                    "bounds": {
                        "bbox": bbox,
                        "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}
                    },
                    "data": [{
                        "type": "sentinel-2-l2a",
                        "dataFilter": {
                            "timeRange": {
                                "from": f"{date}T00:00:00Z",
                                "to": f"{date}T23:59:59Z"
                            }
                        },
                        "maxCloudCoverage": cloud
                    }]
                },
                "output": {
                    "width": width,
                    "height": height,
                    "responses": [{"identifier": "default", "format": {"type": "image/png"}}]
                },
                "evalscript": """
                function setup() {
                return {
                    input: ["B02", "B03", "B04"],
                    output: { bands: 3 }
                };
                }
                function evaluatePixel(sample) {
                return [2.5*sample.B04, 2.5*sample.B03, 2.5*sample.B02];
                }
                """
            }
        
        elif self.radioButton_NBR.isChecked():
            payload = {
                "input": {
                    "bounds": {
                        "bbox": bbox,
                        "properties": {"crs": "http://www.opengis.net/def/crs/EPSG/0/4326"}
                    },
                    "data": [{
                        "type": "sentinel-2-l2a",
                        "dataFilter": {
                            "timeRange": {
                                "from": f"{date}T00:00:00Z",
                                "to": f"{date}T23:59:59Z"
                            }
                        },
                        "maxCloudCoverage": cloud
                    }]
                },
                "output": {
                    "width": width,
                    "height": height,
                    "responses": [{"identifier": "default", "format": {"type": "image/png"}}]
                },
                "evalscript": """
                function setup() {
                return {
                    input: ["B08", "B12"],
                    output: { bands: 1 }
                };
                }
                function evaluatePixel(sample) {
                let nbr = (sample.B08 - sample.B12) / (sample.B08 + sample.B12);
                return [nbr];
                }
                """
            }

        response = requests.post(process_url, headers=headers, json=payload)
        if response.status_code != 200:
            print("Error in the request:", response.text)
            return None

        # Step 3: Convertion in QPixmap
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        return pixmap
    
    def draw_scene(self):
        self.preview_scene.clear()
        self.preview_scene.addPixmap(self.pixmap)
        #self.graphicsView.viewport().update()

    def update_preview(self, bbox, date, cloud, user, password):

        self.pixmap = self.get_sentinel_preview(user, password, bbox, date, cloud)
        if self.pixmap:
            self.draw_scene()
            self.parent().selectRow(self.current_index)
        else:
            print("Impossible to get the image.")

    def go_left(self, bbox, date, cloud, user, password):
        if self.current_index > 0:
            self.current_index -= 1
            date = self.image_list[self.current_index]
            self.update_preview(bbox, date, cloud, user, password)
        else:
            self.leftButton.setEnabled(False)


    def go_right(self, bbox, date, cloud, user, password):
        if self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            date = self.image_list[self.current_index]
            self.update_preview(bbox, date, cloud, user, password)    
        else:
            self.rightButton.setEnabled(False)

