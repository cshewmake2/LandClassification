## Main Method

# import libraries


# import raw images from file locations
#  in: raw_im_file_location, out: raw_im
import_raw()


# import tagged region shape files
#  in: shp_file_location, out: shp_im
import_shp()


# compute indices (~12) from raw_im
#  in: raw_im, out: land_ind
compute_indicies()


# extract tagged regions from raw files
#  in: raw-im, shp-im, out: tag_region
cut_region()


# build matrix of vectorized raw data from tagged regions
  # keep track of class label for each pixel (either in object with pixel val
  # or in lookup relation)

  # in: tag_region, out: learning_set
  #  learning_set resembles:
              #   ind 1   ind 2   ...   ind n
              #    p1       p1            p1
              #    p2       p2            p2
              #                   ....
              #    pk       pk            pk
build_learning_set()

# use learning_set to train the model to differentiate classes based on indicies
# we'll probably design this around whatever library we decide to use for it
    # tensorflow
    # pybrain
    # etc
# of course needs to incorporate splitting the set in to training and testing points
# in: learning_set, params, out: model fitted parameters, error analysis, etc.
learn()

# try applying the classification to the remaining, untagged points on the map
classify()

# view the resulting image
view()
