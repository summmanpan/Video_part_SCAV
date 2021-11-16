# Import functions and libraries
import numpy as np
import matplotlib.pyplot as plt
from imageio import imread
from scipy import fftpack
# Scipy's fftpack module implements the Discrete Cosine Transform,
# an extension of the Fourier Transform that is better suited to
# the compression of real-valued signals - Fourier coefficients
# are complex numbers.


#----------Custom display routines functions-----------------
def display(im):  # Define a new Python routine
    """
    Displays an image using the methods of the 'matplotlib' library.
    """
    plt.figure(figsize=(8,8))                     # Square blackboard
    plt.imshow( im, cmap="gray", vmin=0, vmax=1)  # 'im' using a gray colormap
                                                  #from 0 (black) to 1 (white)
def display_2(im_1, title_1, im_2, title_2):
    """
    Displays two images side by side; typically, an image and its FT.
    """
    plt.figure(figsize=(12,6))                    # Rectangular blackboard
    plt.subplot(1,2,1) ; plt.title(title_1)       # 1x2 waffle plot, 1st cell
    plt.imshow(im_1, cmap="gray")                 # Auto-equalization
    plt.subplot(1,2,2) ; plt.title(title_2)       # 1x2 waffle plot, 2nd cell
    plt.imshow(im_2, cmap="gray", vmin=-7, vmax=15)

#----------Discrete Cosine Transform functions-----------------
#DCT is slightly more adapted to the compression of images than the FT.
def dct2(f):
    """
    Discrete Cosine Transform in 2D.
    """
    return np.transpose(fftpack.dct(
           np.transpose(fftpack.dct(f, norm = "ortho")), norm = "ortho"))

def idct2(f):
    """
    Inverse Discrete Cosine Transform in 2D.
    """
    return np.transpose(fftpack.idct(
           np.transpose(fftpack.idct(f, norm = "ortho")), norm = "ortho"))

#----------small Discrete Cosine Trandforms-----------------
def local_dct(I, w = 8) :  # w = patch size
    lI = np.zeros(I.shape)
    # Loop over the small (w,w) patches ------------------------------
    for i in range(1,I.shape[0]//w+1):
        for j in range(1,I.shape[1]//w+1):
            lI[(i-1)*w: i*w, (j-1)*w: j*w] = dct2(I[(i-1)*w: i*w, (j-1)*w: j*w])
    return lI


def ilocal_dct(lI, w = 8) :  # w = patch size
    I = np.zeros(lI.shape)
    # Loop over the small (w,w) patches ------------------------------
    for i in range(1,I.shape[0]//w+1):
        for j in range(1,I.shape[1]//w+1):
            I[(i-1)*w: i*w, (j-1)*w: j*w] = idct2(lI[(i-1)*w: i*w, (j-1)*w: j*w])
    return I

#----------Solve blocking artifacts-----------------
def lDCT_threshold(lI, threshold):
    lI_thresh = lI.copy()  # Create a copy of the local DCT transform
    lI_thresh[abs(lI) < threshold] = 0  # Remove all the small coefficients
    I_thresh = ilocal_dct(lI_thresh)  # Invert the new transform...

    display_2(I_thresh, "Image",  # And display
              np.log(1e-7 + abs(lI_thresh)), "Local Cosine Transform")
    return I_thresh


if __name__ == '__main__':

    I = imread("data/lena.jpg", as_gray=True)  # Import as a grayscale array
    I = I / 255  # Normalize intensities in the [0,1] range
    I = I[::2, ::2]  # Subsample the image, for convenience

    dI = dct2(I)  # Compute the Cosine Transform of our image

    display_2(I, "Image",
              np.log(1e-7 + abs(dI)), "Cosine Transform (log grayscale)")

    Patch = I[150:182, 100:132]  # Truncate our image...
    dPatch = dct2(Patch)  # And apply a discrete cosine transform

    display_2(Patch, "Image",
              (1e-7 + abs(dPatch)), "Cosine Transform (normal grayscale)")

    lI = local_dct(I, w=8)
    display_2(I, "Image",
              np.log(1e-7 + abs(lI)), "Local Cosine Transform (log grayscale)")

    lDCT_threshold(lI, .5);

    Abs_values = np.sort(abs(lI.ravel()))  # Sort the coefficients' magnitudes
    print(Abs_values)  # in ascending order...

    cutoff = Abs_values[-2000]  # And select the 2000th largest value
    JPEG = lDCT_threshold(lI, cutoff)  # as a cutoff
    display(JPEG)
    plt.savefig('data/compress_dct_img.jpg')
    plt.show()