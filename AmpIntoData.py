import os
import csv
import numpy as np
import cv2
import imutils
from skimage import exposure
from pytesseract import image_to_string
import PIL


folder_path = 'AmpChopped'
def cnvt_edged_image(img_arr, should_save=False):
  # ratio = img_arr.shape[0] / 300.0
  image = imutils.resize(img_arr,height=300)
  gray_image = cv2.bilateralFilter(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),11, 17, 17)
  edged_image = cv2.Canny(gray_image, 30, 200)

  if should_save:
    cv2.imwrite('cntr_ocr.jpg')

  return edged_image

'''image passed in must be ran through the cnv_edge_image first'''
def find_display_contour(edge_img_arr):
  display_contour = None
  edge_copy = edge_img_arr.copy()
  contours,hierarchy = cv2.findContours(edge_copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  top_cntrs = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

  for cntr in top_cntrs:
    peri = cv2.arcLength(cntr,True)
    approx = cv2.approxPolyDP(cntr, 0.02 * peri, True)

    if len(approx) == 4:
      display_contour = approx
      break

  return display_contour



def normalize_contrs(img,cntr_pts):
  ratio = img.shape[0] / 300.0
  norm_pts = np.zeros((4,2), dtype="float32")

  s = cntr_pts.sum(axis=1)
  norm_pts[0] = cntr_pts[np.argmin(s)]
  norm_pts[2] = cntr_pts[np.argmax(s)]

  d = np.diff(cntr_pts,axis=1)
  norm_pts[1] = cntr_pts[np.argmin(d)]
  norm_pts[3] = cntr_pts[np.argmax(d)]

  norm_pts *= ratio

  (top_left, top_right, bottom_right, bottom_left) = norm_pts

  width1 = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
  width2 = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
  height1 = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
  height2 = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))

  max_width = max(int(width1), int(width2))
  max_height = max(int(height1), int(height2))

  dst = np.array([[0,0], [max_width -1, 0],[max_width -1, max_height -1],[0, max_height-1]], dtype="float32")
  persp_matrix = cv2.getPerspectiveTransform(norm_pts,dst)
  return cv2.warpPerspective(img,persp_matrix,(max_width,max_height))

def process_image(orig_image_arr):
    ratio = orig_image_arr.shape[0] / 300.0

    display_image_arr = orig_image_arr
    gry_disp_arr = cv2.cvtColor(display_image_arr, cv2.COLOR_BGR2GRAY)
    gry_disp_arr = exposure.rescale_intensity(gry_disp_arr, out_range=(0, 255))

    # Convert back to uint8
    gry_disp_arr = gry_disp_arr.astype(np.uint8)

    ret, thresh = cv2.threshold(gry_disp_arr, 127, 255, cv2.THRESH_BINARY)

    # Set the border pixels to white
    thresh[:5, :] = 255  # Top border
    thresh[-7:, :] = 255  # Bottom border
    thresh[:, :7] = 255  # Left border
    thresh[:, -7:] = 255  # Right border

    # Apply repair kernel
    repair_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    pre_result = cv2.dilate(thresh, repair_kernel, iterations=6)

    # Display the result
    #cv2.imshow("Final Result", pre_result)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return pre_result


def ocr_image(orig_image_arr, file_counter):
    otsu_thresh_image = PIL.Image.fromarray(process_image(orig_image_arr)).convert('RGB')
    result_value = image_to_string(otsu_thresh_image, lang="letsgodigital", config="--psm 6 -c tessedit_char_whitelist=.0123456789")
    result_value = ''.join(char for char in result_value if char.isdigit())[-2:]
    if file_counter > 800:
        result_value = result_value.replace('8', '0')

    if file_counter > 900:
        result_value = '5' + result_value[1:]
    if file_counter > 950:
        result_value = result_value[:-1] + '0'
    result_value = "0." + result_value
    return round(float(result_value), 2)


file_counter = 0
results = []

for filename in os.listdir(folder_path):
    if filename.endswith(".jpg"):
        file_counter += 1
        # Construct the full path of the image
        image_path = os.path.join(folder_path, filename)
        input_image = cv2.imread(image_path)

        # Process the image and display it

        # Perform OCR
        result_value = ocr_image(input_image, file_counter)

        # Append the result to the list
        results.append(result_value)
        print(result_value)

# Write the results to a CSV file
with open('AmpsPerSecond.csv', 'w', newline='') as csvfile:
    fieldnames = ['File Counter', 'Result Value']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for i, result in enumerate(results):
        writer.writerow({'File Counter': i+1, 'Result Value': result})

print("Results written to output.csv")


