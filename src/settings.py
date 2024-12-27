# -----------------------------------------------------------------------------
#  Project Name: Form Trainer
#  File: settings.py
#  Copyright (C) 2024 Mateus Paiva Fogaca
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  1. Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
#  3. Neither the name of [Your Name or Organization] nor the names of its
#     contributors may be used to endorse or promote products derived from
#     this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING
#  FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
# -----------------------------------------------------------------------------

class Settings:
    def __init__(self):
        # Pose-related settings:
        self.__pose_static_image_mode        = False
        self.__pose_model_complexity         = 1
        self.__pose_min_detection_confidence = 0.5
        self.__pose_min_tracking_confidence  = 0.5

        # GUI-related settings:
        self.__gui_archer_outline_mode       = False

    def pose_static_image_mode(self):
        return self.__pose_static_image_mode

    def set_pose_static_image_mode(self, val):
        self.__pose_static_image_mode = val

    def pose_model_complexity(self):
        return self.__pose_model_complexity

    def set_pose_model_complexity(self, val):
        self.__pose_model_complexity = val

    def pose_min_detection_confidence(self):
        return self.__pose_min_detection_confidence
    
    def set_pose_min_detection_confidence(self, val):
        self.__pose_min_detection_confidence = val
    
    def pose_min_tracking_confidence(self):
        return self.__pose_min_tracking_confidence

    def set_pose_min_tracking_confidence(self, val):
        self.__pose_min_tracking_confidence = val 


global_settings = Settings()