# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: onnx/onnx-data.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from onnx import onnx_ml_pb2 as onnx_dot_onnx__ml__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14onnx/onnx-data.proto\x12\x04onnx\x1a\x12onnx/onnx-ml.proto\"\xf0\x02\n\rSequenceProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\telem_type\x18\x02 \x01(\x05\x12(\n\rtensor_values\x18\x03 \x03(\x0b\x32\x11.onnx.TensorProto\x12\x35\n\x14sparse_tensor_values\x18\x04 \x03(\x0b\x32\x17.onnx.SparseTensorProto\x12,\n\x0fsequence_values\x18\x05 \x03(\x0b\x32\x13.onnx.SequenceProto\x12\"\n\nmap_values\x18\x06 \x03(\x0b\x32\x0e.onnx.MapProto\x12,\n\x0foptional_values\x18\x07 \x03(\x0b\x32\x13.onnx.OptionalProto\"]\n\x08\x44\x61taType\x12\r\n\tUNDEFINED\x10\x00\x12\n\n\x06TENSOR\x10\x01\x12\x11\n\rSPARSE_TENSOR\x10\x02\x12\x0c\n\x08SEQUENCE\x10\x03\x12\x07\n\x03MAP\x10\x04\x12\x0c\n\x08OPTIONAL\x10\x05\"r\n\x08MapProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08key_type\x18\x02 \x01(\x05\x12\x0c\n\x04keys\x18\x03 \x03(\x03\x12\x13\n\x0bstring_keys\x18\x04 \x03(\x0c\x12#\n\x06values\x18\x05 \x01(\x0b\x32\x13.onnx.SequenceProto\"\xeb\x02\n\rOptionalProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\telem_type\x18\x02 \x01(\x05\x12\'\n\x0ctensor_value\x18\x03 \x01(\x0b\x32\x11.onnx.TensorProto\x12\x34\n\x13sparse_tensor_value\x18\x04 \x01(\x0b\x32\x17.onnx.SparseTensorProto\x12+\n\x0esequence_value\x18\x05 \x01(\x0b\x32\x13.onnx.SequenceProto\x12!\n\tmap_value\x18\x06 \x01(\x0b\x32\x0e.onnx.MapProto\x12+\n\x0eoptional_value\x18\x07 \x01(\x0b\x32\x13.onnx.OptionalProto\"]\n\x08\x44\x61taType\x12\r\n\tUNDEFINED\x10\x00\x12\n\n\x06TENSOR\x10\x01\x12\x11\n\rSPARSE_TENSOR\x10\x02\x12\x0c\n\x08SEQUENCE\x10\x03\x12\x07\n\x03MAP\x10\x04\x12\x0c\n\x08OPTIONAL\x10\x05\x42\x02H\x03')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'onnx.onnx_data_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'H\003'
  _SEQUENCEPROTO._serialized_start=51
  _SEQUENCEPROTO._serialized_end=419
  _SEQUENCEPROTO_DATATYPE._serialized_start=326
  _SEQUENCEPROTO_DATATYPE._serialized_end=419
  _MAPPROTO._serialized_start=421
  _MAPPROTO._serialized_end=535
  _OPTIONALPROTO._serialized_start=538
  _OPTIONALPROTO._serialized_end=901
  _OPTIONALPROTO_DATATYPE._serialized_start=326
  _OPTIONALPROTO_DATATYPE._serialized_end=419
# @@protoc_insertion_point(module_scope)
