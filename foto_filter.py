from PIL import Image
import numpy as np
import math
import time

# Here we will the the main menue and the filter menue


class Meny:
    def __init__(self):
        self.status = None
        self.image = None
        self.filter = Filters()

    # Creating the main menue
    def huvud_meny(self):

        # Checking if there is any fil oppen
        if not self.status:
            self.status = "Ingen fil öppen"

        def inner_meny(status):
            huvud_meny = """
            Huvudmeny

            Status: {}

            1. Öppna fil...

            2. Filter

            3. Spara fil som...

            4. Information om programmet

            5. Avsluta
            """.format(status).rstrip()

            return huvud_meny

        # The script will be running as long as the user do not choose leave
        while True:
            meny = inner_meny(self.status)
            print(meny)
            try:
                user_choice = int(input(">> "))
                print("\n")

                if user_choice == 1:
                    # Opening the image, if the file exists. We will change the status, otherwise we will get an erorr
                    try:
                        fil = input("Fil namn: ")
                        self.image = Image.open(fil)
                        self.status = fil
                    except:
                        print("Filen finns inte")

                elif user_choice == 2:
                    # Showing the filter menue
                    if self.status == "Ingen fil öppen":
                        print("Öppna filen först")
                    else:
                        self.filter_meny()
                elif user_choice == 3:

                    if self.status == "Ingen fil öppen":
                        print("Ingen fil är öppen")

                    else:
                        # if any error appears, the script won't break
                        try:
                            # This will save the fil
                            fil_name = input("Spara som: ")
                            self.image.save(fil_name)
                        except Exception as e:
                            print(e)

                elif user_choice == 4:
                    print("A fotofilter program made by Abdulrauf Alhariri ")
                # This will break the whole loop in case the user choose to leave
                elif user_choice == 5:
                    print("Thanks for using the script, Good bye!")
                    return

                else:
                    print("I don't understand")

            except Exception as e:
                print(e)

            time.sleep(2)

    # This function is responsibile for dealing with the filters

    def filter_meny(self):
        filter_meny = """
        Filtermeny

        1. Gråskala

        2. Skifta färgkanaler

        3. Invertera bild

        4. Ljusare (1-10)

        5. Mörkare (1-10)

        6. Pixellera 

        7. Blur

        8. Blend

        9. Back

        """
        print(filter_meny)
        try:
            user_choice = int(input(">>"))
            # Depending on what filter the user choose, we will call it and return the edited image
            if user_choice == 1:
                image = self.filter.grå_skal(self.image)

            elif user_choice == 2:
                image = self.filter.skifta_färgkanaler(self.image)

            elif user_choice == 3:
                image = self.filter.inveter_bild(self.image)

            elif user_choice == 4:
                scale_1_10 = int(
                    input("välja ljusstyrka 1-10? "))
                image = self.filter.brighter(self.image, scale_1_10)

            elif user_choice == 5:
                scale_1_10 = int(
                    input("välja mörkstyrka 1-10? "))
                image = self.filter.darker(self.image, scale_1_10)

            elif user_choice == 6:
                image = self.filter.pixelate(self.image)

            elif user_choice == 7:
                blur_repeats = int(input("Välja suddighets styka (1-4)? "))
                print("Working")
                image = self.filter.blur(2, blur_repeats, self.image)
                print("Done")

            elif user_choice == 8:
                blend_image = input("Ange fil väg till bild två: ")
                try:

                    print("Working")
                    name = self.status
                    image = self.filter.blend_images(name, blend_image)
                    print("Done")

                except Exception as e:
                    print(e)

            # This will take us back to the main menue
            else:
                return

            # Showing the image and asking if the  user want to save it or not
            image.show()
            save_choice = input("Vill du spara filen? (no/yes) ").lower()

            if save_choice == "no":
                # Cecking if the user want to change the filterd image
                keep_or_remove = input(
                    "Vill du få den originala bilden eller vill du forsätta ändra den ändrade bilden?(y/n) ").lower()
                if keep_or_remove == "y":
                    # If the user do not want to save it, so we need to get the original image back.
                    self.image = Image.open(self.status)

                time.sleep(2)
                # So I'm reopining it
                self.filter_meny()

            elif save_choice == "yes":
                saving_name = input("Spara som: ")
                try:
                    # Saving the image, and returning the original image
                    image.save(saving_name)
                    keep_or_remove = input(
                        "Vill du få den originala bilden eller vill du forsätta ändra den ändrade bilden?(y/n) ").lower()
                    if keep_or_remove == "y":
                        # If the user do not want to save it, so we need to get the original image back.
                        self.image = Image.open(self.status)

                except Exception as e:
                    print(e)
                self.filter_meny()

            else:
                print("I don't understand")
                self.filter_meny()

        except Exception as e:
            print(e)


class Filters:

    # Grå skala filtern

    def grå_skal(self, image):

        # for each row in the image we're looping each pixel and changeing it
        try:
            print("Working")
            for y in range(image.height):

                for x in range(image.width):
                    # Getting the old pixel
                    old_pixel = image.getpixel((x, y))

                    # Calculating the average of the rgb colors, by getting the sum of the values and dividing by 3
                    rgb_averge = (
                        old_pixel[0] + old_pixel[1] + old_pixel[2]) // 3
                    red = rgb_averge
                    green = rgb_averge
                    blue = rgb_averge

                    # Creating the new pixel, and replacing the old pixel with the new one
                    new_pixel = (red, green, blue)
                    image.putpixel((x, y), new_pixel)
            print("Done")
            return image
        except Exception as e:
            print(e)

    def skifta_färgkanaler(self, image):
        # Extracting each pixel in the image
        # Then changeing the color channel.
        try:
            print("Working")
            for y in range(image.height):

                for x in range(image.width):
                    old_pixel = image.getpixel((x, y))
                    # Red gets the value of blue
                    red = old_pixel[-1]
                    # Green gets the value of red
                    green = old_pixel[0]
                    # blue gets the value from green
                    blue = old_pixel[1]

                    # Creating the new pixel
                    new_pixel = (red, green, blue)
                    image.putpixel((x, y), new_pixel)
            print("Done")
            return image
        except Exception as e:
            print(e)

    # EN funktion för att nivertera bilder
    def inveter_bild(self, img):
        # Handle errors if there any
        try:
            print("Working")
            # Getting the current cell
            for y in range(img.height):
                for x in range(img.width):
                    old_pixel = img.getpixel((x, y))
                    # subtracting 255 from the current rgb value, and the result will be the new value
                    red = 255 - old_pixel[0]
                    green = 255 - old_pixel[1]
                    blue = 255 - old_pixel[2]

                    # Saving the new pixel
                    new_pixel = (red, green, blue)
                    img.putpixel((x, y), new_pixel)
            print("Done")
            return img
        # Catching the error and print it out
        except Exception as e:

            print(e)

    def darker(self, img, scale_on_1_10):
        # How mush we will decrease the rgb value
        if scale_on_1_10 <= 1:
            decrease_precentage = 0

        elif scale_on_1_10 >= 10:
            decrease_precentage = 0.99

        else:
            decrease_precentage = scale_on_1_10 / 10

        # Decreasing the rgb value in each pixel, with the precentage that we got from the user
        for y in range(img.height):
            for x in range(img.width):
                old_pixel = img.getpixel((x, y))

                # Here by subtracting 255 from the current rgb value and then multiplacting it with the precentage value
                # that we got above
                decrease_r = (255 - old_pixel[0])*decrease_precentage
                decrease_g = (255 - old_pixel[1])*decrease_precentage
                decrease_b = (255 - old_pixel[2])*decrease_precentage

                # Getting the new value
                red = math.floor(old_pixel[0] - decrease_r)
                green = math.floor(old_pixel[1] - decrease_g)
                blue = math.floor(old_pixel[2] - decrease_b)

                new_pixel = (red, green, blue)
                img.putpixel((x, y), new_pixel)

        return img

    def brighter(self, img, scale_on_1_10):
        # How mush we will descrease the rgb value
        if scale_on_1_10 <= 1:
            increase_precentage = 0

        elif scale_on_1_10 >= 10:
            increase_precentage = 0.99

        else:
            increase_precentage = scale_on_1_10 / 10

        print("Working")
        # Descreasing the rgb value in each pixel, with the precentage that we got from the user
        for y in range(img.height):
            for x in range(img.width):
                old_pixel = img.getpixel((x, y))

                # Here by subtracting 255 from the current rgb value and then multiplacting it with the precentage value
                # that we got above
                increase_r = (255 - old_pixel[0])*increase_precentage
                increase_g = (255 - old_pixel[1])*increase_precentage
                increase_b = (255 - old_pixel[2])*increase_precentage

                # Increasing the rgb values, so it will be brighter
                red = math.floor(old_pixel[0] + increase_r)
                green = math.floor(old_pixel[1] + increase_g)
                blue = math.floor(old_pixel[2] + increase_b)

                new_pixel = (red, green, blue)
                img.putpixel((x, y), new_pixel)
        print("Done")
        return img

    # A function to pixelate an image

    def pixelate(self, image):
        try:
            print("Working")
            # Converting the image into a matrix
            imgArray = np.asarray(image)

            # Getting the height and width
            img_height = imgArray.shape[0]
            img_width = imgArray.shape[1]

            # Bluring window
            pixelate_window = 20

            # Creating a new img, there we will store the new pixels. Its a 3D list with zeros
            img_b = np.zeros((img_height, img_width, 3), np.uint8)
            img_c = np.zeros((img_height, img_width, 3), np.uint8)

            # Pixelating the image horizintally
            for row in range(img_height):

                total_r = 0
                total_g = 0
                total_b = 0
                # Looping as long there is some pixels that has not been changed
                for i in range(0, img_width, pixelate_window):
                    # Getting the current pixel
                    for co in range(pixelate_window):
                        # Here we make sure that we start from the place we end
                        co += i
                        # To check if we are at the last pixel, otherwise we will get an error
                        if co <= img_width - 1:
                            # Getting the averge rgb values
                            total_r += imgArray[row][co][0]/pixelate_window
                            total_g += imgArray[row][co][1]/pixelate_window
                            total_b += imgArray[row][co][2]/pixelate_window

                    # Replacing the rgb values of the pixels in the window to the averge rgb values
                    for co in range(pixelate_window):
                        co += i
                        if co <= img_width - 1:
                            img_b[row][co][0] = total_r
                            img_b[row][co][1] = total_g
                            img_b[row][co][2] = total_b

                    # resetting the averge values to 0
                    total_r -= total_r
                    total_g -= total_g
                    total_b -= total_b

            # Pixelating the image vertically
            for co in range(img_width):
                total_r = 0
                total_g = 0
                total_b = 0

                for i in range(0, img_width, pixelate_window):
                    # Pixelating the first 100 pixels in the image
                    for row in range(pixelate_window):
                        row += i
                        if row <= img_height - 1:
                            # Getting the averge rgb values
                            total_r += img_b[row][co][0]/pixelate_window
                            total_g += img_b[row][co][1]/pixelate_window
                            total_b += img_b[row][co][2]/pixelate_window

                    # Replacing the rgb values of the pixels in the window to the averge rgb values
                    for row in range(pixelate_window):
                        row += i
                        if row <= img_height - 1:
                            img_c[row][co][0] = total_r
                            img_c[row][co][1] = total_g
                            img_c[row][co][2] = total_b

                    # resetting the averge values to 0
                    total_r -= total_r
                    total_g -= total_g
                    total_b -= total_b

            # Creating the image
            img_c = Image.fromarray(np.uint8(img_c))
            # Returning the image so we can save it or show it
            print("Done")
            return img_c
        except Exception as e:
            print(e)

    # A function to blur an image

    def blur(self, radius, repeats, image):
        try:
            repeats -= 1
            # Converting the image into a matrix
            imgArray = np.asarray(image)

            # Getting the height and width
            img_height = imgArray.shape[0]
            img_width = imgArray.shape[1]

            # Bluring window
            blur_window = radius*2+1

            # Creating a new img, there we will store the new pixels. Its a 3D list with zeros
            img_b = np.zeros((img_height, img_width, 3), np.uint8)
            img_c = np.zeros((img_height, img_width, 3), np.uint8)

            # To make the bluring faster so we are going to blur it horizintally and then vertically
            # Bluring horizontally
            for row in range(img_height):
                # print(row)
                total_r = 0
                total_g = 0
                total_b = 0

                # Calculating the averge pixel of the first pixel in each row
                for c in range(-radius, radius + 1):
                    # We check that we start removing from pixel 0, because we don't have any pixels before pixel 0
                    if (c) >= 0 and (c) <= img_width-1:
                        total_r += imgArray[row][c][0]/blur_window
                        total_g += imgArray[row][c][1]/blur_window
                        total_b += imgArray[row][c][2]/blur_window

                img_b[row, 0] = [total_r, total_g, total_b]

                # Because we move forward and then calculate the nex pixel in the row, so we just subtract the leaving pixel
                # And add the next pixel
                for co in range(1, img_width):
                    # Checking that we start removing from cell one in the row
                    if (co-radius-1) >= 0:
                        # Removing the leaving pixel,  Subtracting its averge value from the total
                        total_r -= imgArray[row][co-radius - 1][0]/blur_window
                        total_g -= imgArray[row][co -
                                                 radius - 1][1] / blur_window
                        total_b -= imgArray[row][co -
                                                 radius - 1][2] / blur_window
                    if (co+radius) <= img_width-1:
                        # Adding the averge value of the next pixel to the summ
                        total_r += imgArray[row][co+radius][0]/blur_window
                        total_g += imgArray[row][co+radius][1]/blur_window
                        total_b += imgArray[row][co+radius][2]/blur_window

                    # Creating the new pixel
                    img_b[row][co] = [total_r,
                                      total_g, total_b]

            # Bluring verticly
            for coulmn in range(img_width):
                # print(coulmn)
                total_r = 0
                total_g = 0
                total_b = 0

                # Calculating the averge pixel of the first pixel in the first row
                for row in range(-radius, radius+1):
                    if (row) >= 0 and (row) <= img_height-1:
                        total_r += img_b[row][coulmn][0]/blur_window
                        total_g += img_b[row][coulmn][1]/blur_window
                        total_b += img_b[row][coulmn][2]/blur_window

                # Saving the pixel in the array
                img_c[0][coulmn] = [total_r, total_g, total_b]

                # Looping each row and calculating the averge rgb value of the current pixel in each row
                for r in range(1, img_height):
                    if (r-radius-1) >= 0:
                        # Subtracting the leaving pixel
                        total_r -= img_b[r - radius-1][coulmn][0] / blur_window
                        total_g -= img_b[r-radius-1][coulmn][1]/blur_window
                        total_b -= img_b[r-radius-1][coulmn][2]/blur_window

                    if r + radius <= img_height - 1:
                        # Adding the next pixel
                        total_r += img_b[r+radius][coulmn][0] / blur_window
                        total_g += img_b[r+radius][coulmn][1]/blur_window
                        total_b += img_b[r+radius][coulmn][2]/blur_window

                    # Saving the pixel
                    img_c[r][coulmn] = [
                        total_r, total_g, total_b]
        except Exception as e:
            print(e)

        # Bluring a few times before saving the image
        image = Image.fromarray(np.uint8(img_c))
        if repeats > 0:
            return self.blur(2, repeats, image)

        return image

    # A function to combine two images
    def blend_images(self, image_1, image_2):
        image_1 = Image.open(image_1)
        image_2 = Image.open(image_2)

        # Converting them to an array
        img1_arr = np.asarray(image_1)
        img2_arr = np.asarray(image_2)

        img1_img2 = img1_arr

        # Converting it to float, the purpose is to see the alpha channel, if it is fully displayed or not
        # Because the opcity is between 0-1 and in this case 0-255
        img1_arr = img1_arr.astype(float) / 255
        img2_arr = img2_arr.astype(float) / 255

        # Getting the height and width
        img_height = img1_arr.shape[0]
        img_width = img1_arr.shape[1]

        # Checking if any rgb value is less than 0.5
        opacity_low = img1_arr < 0.5

        # Here we will save the blend image, defining a matrix of the same demension as imge_1
        blend_img = np.zeros_like(img1_arr)

        for y in range(img_height):
            for x in range(img_width):
                # This is the first implementation of the overlay algorithim
                # Getting the current pixel in each array
                cuurent_opcity = opacity_low[y][x]
                current_px_img1 = img1_arr[y][x]
                current_px_img2 = img2_arr[y][x]
                current_px_blend_img = blend_img[y][x]

                # Looping and checking each rgb value, if it is less than 0.5 or higher
                for i in range(3):
                    # If it true, the dark pixels becomes darker
                    if cuurent_opcity[i]:
                        # This will make the pixels darker, and mixe it
                        current_px_blend_img[i] = 2 * \
                            current_px_img1[i]*current_px_img2[i]

                    # Else it is more than 0.5, so the pixels becomes brighter
                    else:
                        # This will make it brighter, and mixe it
                        current_px_blend_img[i] = (1-2*(1-current_px_img1[i])
                                                   * (1-current_px_img2[i]))

                # An another implementation of the algorithim
                # current_px_img1_img2 = img1_img2[y][x]
                # current_px_img1 = img1_arr[y][x]
                # current_px_img2 = img2_arr[y][x]
                # for i in range(3):
                #     current_px_img1_img2[i] = current_px_img1[i] + \
                #         current_px_img2[i]

        # Converting the results to rgb, by multiplacating them by 255
        finall_version_img = (blend_img*255).astype(np.uint8)
        image = Image.fromarray(np.uint8(finall_version_img))
        return image


# This we make sure that the script will run in the main program. So if you import it this we not run automaticly
if __name__ == "__main__":
    meny = Meny()
    meny.huvud_meny()
