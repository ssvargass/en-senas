from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io
import socket
import struct
import json
from PIL import Image
import tensorflow as tf
import requests as rq


import os.path
import re


import numpy as np


FLAGS = tf.app.flags.FLAGS

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('en-senas.org', 8080))
server_socket.listen(5)

# Accept a single connection and make a file-like object out of it
# connection = server_socket.accept()[0].makefile('rb')



tf.app.flags.DEFINE_string(
    'model_dir', '/home/svargas/en-senas/raspberrypi',
    """Path to classify_image_graph_def.pb, """
    """imagenet_synset_to_human_label_map.txt, and """
    """imagenet_2012_challenge_label_map_proto.pbtxt.""")

tf.app.flags.DEFINE_integer('num_top_predictions', 5,
                            """Display this many predictions.""")

class NodeLookup(object):
  """Converts integer node ID's to human readable labels."""

  def __init__(self,
               label_lookup_path=None,
               uid_lookup_path=None):
    if not label_lookup_path:
      label_lookup_path = os.path.join(
          FLAGS.model_dir, 'imagenet_2012_challenge_label_map_proto.pbtxt')
    if not uid_lookup_path:
      uid_lookup_path = os.path.join(
          FLAGS.model_dir, 'imagenet_synset_to_human_label_map.txt')
    self.node_lookup = self.load(label_lookup_path, uid_lookup_path)

  def load(self, label_lookup_path, uid_lookup_path):
    """Loads a human readable English name for each softmax node.
    Args:
      label_lookup_path: string UID to integer node ID.
      uid_lookup_path: string UID to human-readable string.
    Returns:
      dict from integer node ID to human-readable string.
    """
    if not tf.gfile.Exists(uid_lookup_path):
      tf.logging.fatal('File does not exist %s', uid_lookup_path)
    if not tf.gfile.Exists(label_lookup_path):
      tf.logging.fatal('File does not exist %s', label_lookup_path)

    # Loads mapping from string UID to human-readable string
    proto_as_ascii_lines = tf.gfile.GFile(uid_lookup_path).readlines()
    uid_to_human = {}
    p = re.compile(r'[n\d]*[ \S,]*')
    for line in proto_as_ascii_lines:
      parsed_items = p.findall(line)
      uid = parsed_items[0]
      human_string = parsed_items[2]
      uid_to_human[uid] = human_string

    # Loads mapping from string UID to integer node ID.
    node_id_to_uid = {}
    proto_as_ascii = tf.gfile.GFile(label_lookup_path).readlines()
    for line in proto_as_ascii:
      if line.startswith('  target_class:'):
        target_class = int(line.split(': ')[1])
      if line.startswith('  target_class_string:'):
        target_class_string = line.split(': ')[1]
        node_id_to_uid[target_class] = target_class_string[1:-2]

    # Loads the final mapping of integer node ID to human-readable string
    node_id_to_name = {}
    for key, val in node_id_to_uid.items():
      if val not in uid_to_human:
        tf.logging.fatal('Failed to locate: %s', val)
      name = uid_to_human[val]
      node_id_to_name[key] = name

    return node_id_to_name

  def id_to_string(self, node_id):
    if node_id not in self.node_lookup:
      return ''
    return self.node_lookup[node_id]


def create_graph():
  """Creates a graph from saved GraphDef file and returns a saver."""
  # Creates graph from saved graph_def.pb.
  with tf.gfile.FastGFile(os.path.join(
      FLAGS.model_dir, 'classify_image_graph_def.pb'), 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

while 1:
    (conn, addr) = server_socket.accept()
    connection = conn.makefile('rb')
    print(connection)
    image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
    image_stream = io.BytesIO()
    image_stream.write(connection.read(image_len))
    # # Rewind the stream, open it as an image with PIL and do some
    # # processing on it
    image_stream.seek(0)
    image = Image.open(image_stream)
    image.save('scan.jpg')

    image_data = tf.gfile.FastGFile('scan.jpg', 'rb').read()
    create_graph()
    with tf.Session() as sess:
        # Some useful tensors:
        # 'softmax:0': A tensor containing the normalized prediction across
        #   1000 labels.
        # 'pool_3:0': A tensor containing the next-to-last layer containing 2048
        #   float description of the image.
        # 'DecodeJpeg/contents:0': A tensor containing a string providing JPEG
        #   encoding of the image.
        # Runs the softmax tensor by feeding the image_data as input to the graph.
        softmax_tensor = sess.graph.get_tensor_by_name('softmax:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        # Creates node ID --> English string lookup.
        node_lookup = NodeLookup()

        top_k = predictions.argsort()[-FLAGS.num_top_predictions:][::-1]
        human_string = []
        for node_id in top_k:
          text = node_lookup.id_to_string(node_id)
          text = re.split('\W+', text)
          human_string += text
          #score = predictions[node_id]
          #print('%s (score = %.5f)' % (human_string, score))

        djangotext = ','.join(human_string)
	print(djangotext)
        r = rq.get('http://en-senas.org/words?tag=' + djangotext)
        if(r.status_code == 200):
            dictionary = json.loads(r.text)
            print(dictionary)
            if(dictionary['count'] == 0):
                tpm_dict = {
                    'image': '',
                    'title': 'No tenemos resultados'
                }
                dictionary['results'].append(tpm_dict)
            conn.send(str(dictionary['results'][0]))
	    conn.close()
	else:
	    tpm_dict = {
                'image': '',
                'title': 'No tenemos resultados'
            }
	    conn.send(str(tpm_dict))
	    conn.close()
