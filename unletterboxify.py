from pathlib import Path
from statistics import median

from moviepy.video.fx.crop import crop
from moviepy.video.io.VideoFileClip import VideoFileClip
from sys import argv

# Videos aren't perfect with color, so if it's mostly black ignore it
R_THRESHOLD = 7
G_THRESHOLD = 7
B_THRESHOLD = 7


def get_left_edge(frame) -> int:
    height = len(frame)
    width = len(frame[0])

    for column in range(width):
        for row in range(height):
            if frame[row][column][0] > R_THRESHOLD or \
                    frame[row][column][1] > G_THRESHOLD or \
                    frame[row][column][2] > B_THRESHOLD:
                return column


def get_right_edge(frame, width: int = None, height: int = None) -> int:
    if height is None:
        height = len(frame)

    if width is None:
        width = len(frame[0])

    for column in reversed(range(width)):
        for row in range(height):
            if frame[row][column][0] > R_THRESHOLD or \
                    frame[row][column][1] > G_THRESHOLD or \
                    frame[row][column][2] > B_THRESHOLD:
                return column


def get_bottom_edge(frame) -> int:
    height = len(frame)
    width = len(frame[0])

    for row in range(height):
        for column in range(width):
            if frame[row][column][0] > R_THRESHOLD or \
                    frame[row][column][1] > G_THRESHOLD or \
                    frame[row][column][2] > B_THRESHOLD:
                return row


def get_top_edge(frame, width: int = None, height: int = None) -> int:
    if height is None:
        height = len(frame)

    if width is None:
        width = len(frame[0])

    for row in reversed(range(height)):
        for column in range(width):
            if frame[row][column][0] > R_THRESHOLD or \
                    frame[row][column][1] > G_THRESHOLD or \
                    frame[row][column][2] > B_THRESHOLD:
                return row


def main(path: str) -> int:
    path = Path(path)

    if not path.exists():
        print("Not a valid path")
        return (2)

    with VideoFileClip(str(path)) as clip:
        first_frame = clip.get_frame(0)
        middle_frame = clip.get_frame(clip.duration / 2)
        # I don't know exactly where the last frame is, so rounding down to the next whole number is probably good
        # enough for this
        last_frame = clip.get_frame(round(clip.duration, 0))

        height = len(first_frame)
        width = len(first_frame[0])
        print(f"Original resolution: {width}x{height}")

        # Magic of cache I call on you now, check these three frames one at a time
        first_left = get_left_edge(first_frame)
        first_right = get_right_edge(first_frame)
        first_top = get_top_edge(first_frame)
        first_bottom = get_bottom_edge(first_frame)

        middle_left = get_left_edge(middle_frame)
        middle_right = get_right_edge(middle_frame)
        middle_top = get_top_edge(middle_frame)
        middle_bottom = get_bottom_edge(middle_frame)

        last_left = get_left_edge(last_frame)
        last_right = get_right_edge(last_frame)
        last_top = get_top_edge(last_frame)
        last_bottom = get_bottom_edge(last_frame)

        # If the beginning of the video is a loading screen/fading into a scene, it may have many black pixels. Sample
        # three frames to try to figure out what size the video is supposed to be. Taking the median because video
        # encoding isn't perfect, and black pixels might not be entirely black
        left_edge = median([first_left, middle_left, last_left])
        right_edge = median([first_right, middle_right, last_right])
        top_edge = median([first_top, middle_top, last_top])
        bottom_edge = median([first_bottom, middle_bottom, last_bottom])

        print(f"Cropped resolution: {right_edge - left_edge + 1}x{top_edge - bottom_edge + 1}")
        #print(left_edge)
        #print(right_edge)
        #print(top_edge)
        #print(bottom_edge)

        cropped_clip = crop(clip, x1=left_edge, y1=bottom_edge, x2=right_edge, y2=top_edge)

        cropped_clip.write_videofile(str(path.with_suffix("")) + "_cropped" + str(path.suffix))

        return(0)

if __name__ == "__main__":
    if len(argv) != 2:
        print("Expects exactly 1 argument: filename")
        exit(1)
    exit(main(argv[1]))
