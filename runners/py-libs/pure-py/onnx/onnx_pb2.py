# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: onnx/onnx-ml.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12onnx/onnx-ml.proto\x12\x04onnx\"\xdb\x05\n\x0e\x41ttributeProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x15\n\rref_attr_name\x18\x15 \x01(\t\x12\x12\n\ndoc_string\x18\r \x01(\t\x12\x30\n\x04type\x18\x14 \x01(\x0e\x32\".onnx.AttributeProto.AttributeType\x12\t\n\x01\x66\x18\x02 \x01(\x02\x12\t\n\x01i\x18\x03 \x01(\x03\x12\t\n\x01s\x18\x04 \x01(\x0c\x12\x1c\n\x01t\x18\x05 \x01(\x0b\x32\x11.onnx.TensorProto\x12\x1b\n\x01g\x18\x06 \x01(\x0b\x32\x10.onnx.GraphProto\x12.\n\rsparse_tensor\x18\x16 \x01(\x0b\x32\x17.onnx.SparseTensorProto\x12\x1b\n\x02tp\x18\x0e \x01(\x0b\x32\x0f.onnx.TypeProto\x12\x0e\n\x06\x66loats\x18\x07 \x03(\x02\x12\x0c\n\x04ints\x18\x08 \x03(\x03\x12\x0f\n\x07strings\x18\t \x03(\x0c\x12\"\n\x07tensors\x18\n \x03(\x0b\x32\x11.onnx.TensorProto\x12 \n\x06graphs\x18\x0b \x03(\x0b\x32\x10.onnx.GraphProto\x12/\n\x0esparse_tensors\x18\x17 \x03(\x0b\x32\x17.onnx.SparseTensorProto\x12$\n\x0btype_protos\x18\x0f \x03(\x0b\x32\x0f.onnx.TypeProto\"\xd9\x01\n\rAttributeType\x12\r\n\tUNDEFINED\x10\x00\x12\t\n\x05\x46LOAT\x10\x01\x12\x07\n\x03INT\x10\x02\x12\n\n\x06STRING\x10\x03\x12\n\n\x06TENSOR\x10\x04\x12\t\n\x05GRAPH\x10\x05\x12\x11\n\rSPARSE_TENSOR\x10\x0b\x12\x0e\n\nTYPE_PROTO\x10\r\x12\n\n\x06\x46LOATS\x10\x06\x12\x08\n\x04INTS\x10\x07\x12\x0b\n\x07STRINGS\x10\x08\x12\x0b\n\x07TENSORS\x10\t\x12\n\n\x06GRAPHS\x10\n\x12\x12\n\x0eSPARSE_TENSORS\x10\x0c\x12\x0f\n\x0bTYPE_PROTOS\x10\x0eJ\x04\x08\x0c\x10\rJ\x04\x08\x10\x10\x14R\x01v\"\x87\x01\n\x0eValueInfoProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x1d\n\x04type\x18\x02 \x01(\x0b\x32\x0f.onnx.TypeProto\x12\x12\n\ndoc_string\x18\x03 \x01(\t\x12\x34\n\x0emetadata_props\x18\x04 \x03(\x0b\x32\x1c.onnx.StringStringEntryProto\"\xde\x01\n\tNodeProto\x12\r\n\x05input\x18\x01 \x03(\t\x12\x0e\n\x06output\x18\x02 \x03(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\x0f\n\x07op_type\x18\x04 \x01(\t\x12\x0e\n\x06\x64omain\x18\x07 \x01(\t\x12\x10\n\x08overload\x18\x08 \x01(\t\x12\'\n\tattribute\x18\x05 \x03(\x0b\x32\x14.onnx.AttributeProto\x12\x12\n\ndoc_string\x18\x06 \x01(\t\x12\x34\n\x0emetadata_props\x18\t \x03(\x0b\x32\x1c.onnx.StringStringEntryProto\"\xd6\x01\n\x11TrainingInfoProto\x12(\n\x0einitialization\x18\x01 \x01(\x0b\x32\x10.onnx.GraphProto\x12#\n\talgorithm\x18\x02 \x01(\x0b\x32\x10.onnx.GraphProto\x12<\n\x16initialization_binding\x18\x03 \x03(\x0b\x32\x1c.onnx.StringStringEntryProto\x12\x34\n\x0eupdate_binding\x18\x04 \x03(\x0b\x32\x1c.onnx.StringStringEntryProto\"\xeb\x02\n\nModelProto\x12\x12\n\nir_version\x18\x01 \x01(\x03\x12.\n\x0copset_import\x18\x08 \x03(\x0b\x32\x18.onnx.OperatorSetIdProto\x12\x15\n\rproducer_name\x18\x02 \x01(\t\x12\x18\n\x10producer_version\x18\x03 \x01(\t\x12\x0e\n\x06\x64omain\x18\x04 \x01(\t\x12\x15\n\rmodel_version\x18\x05 \x01(\x03\x12\x12\n\ndoc_string\x18\x06 \x01(\t\x12\x1f\n\x05graph\x18\x07 \x01(\x0b\x32\x10.onnx.GraphProto\x12\x34\n\x0emetadata_props\x18\x0e \x03(\x0b\x32\x1c.onnx.StringStringEntryProto\x12.\n\rtraining_info\x18\x14 \x03(\x0b\x32\x17.onnx.TrainingInfoProto\x12&\n\tfunctions\x18\x19 \x03(\x0b\x32\x13.onnx.FunctionProto\"4\n\x16StringStringEntryProto\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"k\n\x10TensorAnnotation\x12\x13\n\x0btensor_name\x18\x01 \x01(\t\x12\x42\n\x1cquant_parameter_tensor_names\x18\x02 \x03(\x0b\x32\x1c.onnx.StringStringEntryProto\"\xd4\x03\n\nGraphProto\x12\x1d\n\x04node\x18\x01 \x03(\x0b\x32\x0f.onnx.NodeProto\x12\x0c\n\x04name\x18\x02 \x01(\t\x12&\n\x0binitializer\x18\x05 \x03(\x0b\x32\x11.onnx.TensorProto\x12\x33\n\x12sparse_initializer\x18\x0f \x03(\x0b\x32\x17.onnx.SparseTensorProto\x12\x12\n\ndoc_string\x18\n \x01(\t\x12#\n\x05input\x18\x0b \x03(\x0b\x32\x14.onnx.ValueInfoProto\x12$\n\x06output\x18\x0c \x03(\x0b\x32\x14.onnx.ValueInfoProto\x12(\n\nvalue_info\x18\r \x03(\x0b\x32\x14.onnx.ValueInfoProto\x12\x37\n\x17quantization_annotation\x18\x0e \x03(\x0b\x32\x16.onnx.TensorAnnotation\x12\x34\n\x0emetadata_props\x18\x10 \x03(\x0b\x32\x1c.onnx.StringStringEntryProtoJ\x04\x08\x03\x10\x04J\x04\x08\x04\x10\x05J\x04\x08\x06\x10\nR\nir_versionR\x10producer_versionR\x0cproducer_tagR\x06\x64omain\"\xcd\x06\n\x0bTensorProto\x12\x0c\n\x04\x64ims\x18\x01 \x03(\x03\x12\x11\n\tdata_type\x18\x02 \x01(\x05\x12*\n\x07segment\x18\x03 \x01(\x0b\x32\x19.onnx.TensorProto.Segment\x12\x16\n\nfloat_data\x18\x04 \x03(\x02\x42\x02\x10\x01\x12\x16\n\nint32_data\x18\x05 \x03(\x05\x42\x02\x10\x01\x12\x13\n\x0bstring_data\x18\x06 \x03(\x0c\x12\x16\n\nint64_data\x18\x07 \x03(\x03\x42\x02\x10\x01\x12\x0c\n\x04name\x18\x08 \x01(\t\x12\x12\n\ndoc_string\x18\x0c \x01(\t\x12\x10\n\x08raw_data\x18\t \x01(\x0c\x12\x33\n\rexternal_data\x18\r \x03(\x0b\x32\x1c.onnx.StringStringEntryProto\x12\x35\n\rdata_location\x18\x0e \x01(\x0e\x32\x1e.onnx.TensorProto.DataLocation\x12\x17\n\x0b\x64ouble_data\x18\n \x03(\x01\x42\x02\x10\x01\x12\x17\n\x0buint64_data\x18\x0b \x03(\x04\x42\x02\x10\x01\x12\x34\n\x0emetadata_props\x18\x10 \x03(\x0b\x32\x1c.onnx.StringStringEntryProto\x1a%\n\x07Segment\x12\r\n\x05\x62\x65gin\x18\x01 \x01(\x03\x12\x0b\n\x03\x65nd\x18\x02 \x01(\x03\"\xb9\x02\n\x08\x44\x61taType\x12\r\n\tUNDEFINED\x10\x00\x12\t\n\x05\x46LOAT\x10\x01\x12\t\n\x05UINT8\x10\x02\x12\x08\n\x04INT8\x10\x03\x12\n\n\x06UINT16\x10\x04\x12\t\n\x05INT16\x10\x05\x12\t\n\x05INT32\x10\x06\x12\t\n\x05INT64\x10\x07\x12\n\n\x06STRING\x10\x08\x12\x08\n\x04\x42OOL\x10\t\x12\x0b\n\x07\x46LOAT16\x10\n\x12\n\n\x06\x44OUBLE\x10\x0b\x12\n\n\x06UINT32\x10\x0c\x12\n\n\x06UINT64\x10\r\x12\r\n\tCOMPLEX64\x10\x0e\x12\x0e\n\nCOMPLEX128\x10\x0f\x12\x0c\n\x08\x42\x46LOAT16\x10\x10\x12\x10\n\x0c\x46LOAT8E4M3FN\x10\x11\x12\x12\n\x0e\x46LOAT8E4M3FNUZ\x10\x12\x12\x0e\n\nFLOAT8E5M2\x10\x13\x12\x12\n\x0e\x46LOAT8E5M2FNUZ\x10\x14\x12\t\n\x05UINT4\x10\x15\x12\x08\n\x04INT4\x10\x16\")\n\x0c\x44\x61taLocation\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\x0c\n\x08\x45XTERNAL\x10\x01\"h\n\x11SparseTensorProto\x12!\n\x06values\x18\x01 \x01(\x0b\x32\x11.onnx.TensorProto\x12\"\n\x07indices\x18\x02 \x01(\x0b\x32\x11.onnx.TensorProto\x12\x0c\n\x04\x64ims\x18\x03 \x03(\x03\"\x95\x01\n\x10TensorShapeProto\x12-\n\x03\x64im\x18\x01 \x03(\x0b\x32 .onnx.TensorShapeProto.Dimension\x1aR\n\tDimension\x12\x13\n\tdim_value\x18\x01 \x01(\x03H\x00\x12\x13\n\tdim_param\x18\x02 \x01(\tH\x00\x12\x12\n\ndenotation\x18\x03 \x01(\tB\x07\n\x05value\"\xa5\x05\n\tTypeProto\x12-\n\x0btensor_type\x18\x01 \x01(\x0b\x32\x16.onnx.TypeProto.TensorH\x00\x12\x31\n\rsequence_type\x18\x04 \x01(\x0b\x32\x18.onnx.TypeProto.SequenceH\x00\x12\'\n\x08map_type\x18\x05 \x01(\x0b\x32\x13.onnx.TypeProto.MapH\x00\x12\x31\n\roptional_type\x18\t \x01(\x0b\x32\x18.onnx.TypeProto.OptionalH\x00\x12:\n\x12sparse_tensor_type\x18\x08 \x01(\x0b\x32\x1c.onnx.TypeProto.SparseTensorH\x00\x12-\n\x0bopaque_type\x18\x07 \x01(\x0b\x32\x16.onnx.TypeProto.OpaqueH\x00\x12\x12\n\ndenotation\x18\x06 \x01(\t\x1a\x42\n\x06Tensor\x12\x11\n\telem_type\x18\x01 \x01(\x05\x12%\n\x05shape\x18\x02 \x01(\x0b\x32\x16.onnx.TensorShapeProto\x1a.\n\x08Sequence\x12\"\n\telem_type\x18\x01 \x01(\x0b\x32\x0f.onnx.TypeProto\x1a<\n\x03Map\x12\x10\n\x08key_type\x18\x01 \x01(\x05\x12#\n\nvalue_type\x18\x02 \x01(\x0b\x32\x0f.onnx.TypeProto\x1a.\n\x08Optional\x12\"\n\telem_type\x18\x01 \x01(\x0b\x32\x0f.onnx.TypeProto\x1aH\n\x0cSparseTensor\x12\x11\n\telem_type\x18\x01 \x01(\x05\x12%\n\x05shape\x18\x02 \x01(\x0b\x32\x16.onnx.TensorShapeProto\x1a&\n\x06Opaque\x12\x0e\n\x06\x64omain\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\tB\x07\n\x05value\"5\n\x12OperatorSetIdProto\x12\x0e\n\x06\x64omain\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x03\"\x86\x03\n\rFunctionProto\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\r\n\x05input\x18\x04 \x03(\t\x12\x0e\n\x06output\x18\x05 \x03(\t\x12\x11\n\tattribute\x18\x06 \x03(\t\x12-\n\x0f\x61ttribute_proto\x18\x0b \x03(\x0b\x32\x14.onnx.AttributeProto\x12\x1d\n\x04node\x18\x07 \x03(\x0b\x32\x0f.onnx.NodeProto\x12\x12\n\ndoc_string\x18\x08 \x01(\t\x12.\n\x0copset_import\x18\t \x03(\x0b\x32\x18.onnx.OperatorSetIdProto\x12\x0e\n\x06\x64omain\x18\n \x01(\t\x12\x10\n\x08overload\x18\r \x01(\t\x12(\n\nvalue_info\x18\x0c \x03(\x0b\x32\x14.onnx.ValueInfoProto\x12\x34\n\x0emetadata_props\x18\x0e \x03(\x0b\x32\x1c.onnx.StringStringEntryProtoJ\x04\x08\x02\x10\x03J\x04\x08\x03\x10\x04R\rsince_versionR\x06status*\x97\x02\n\x07Version\x12\x12\n\x0e_START_VERSION\x10\x00\x12\x19\n\x15IR_VERSION_2017_10_10\x10\x01\x12\x19\n\x15IR_VERSION_2017_10_30\x10\x02\x12\x18\n\x14IR_VERSION_2017_11_3\x10\x03\x12\x18\n\x14IR_VERSION_2019_1_22\x10\x04\x12\x18\n\x14IR_VERSION_2019_3_18\x10\x05\x12\x18\n\x14IR_VERSION_2019_9_19\x10\x06\x12\x17\n\x13IR_VERSION_2020_5_8\x10\x07\x12\x18\n\x14IR_VERSION_2021_7_30\x10\x08\x12\x17\n\x13IR_VERSION_2023_5_5\x10\t\x12\x0e\n\nIR_VERSION\x10\n*.\n\x0eOperatorStatus\x12\x10\n\x0c\x45XPERIMENTAL\x10\x00\x12\n\n\x06STABLE\x10\x01\x42\x02H\x03')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'onnx.onnx_ml_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'H\003'
  _TENSORPROTO.fields_by_name['float_data']._options = None
  _TENSORPROTO.fields_by_name['float_data']._serialized_options = b'\020\001'
  _TENSORPROTO.fields_by_name['int32_data']._options = None
  _TENSORPROTO.fields_by_name['int32_data']._serialized_options = b'\020\001'
  _TENSORPROTO.fields_by_name['int64_data']._options = None
  _TENSORPROTO.fields_by_name['int64_data']._serialized_options = b'\020\001'
  _TENSORPROTO.fields_by_name['double_data']._options = None
  _TENSORPROTO.fields_by_name['double_data']._serialized_options = b'\020\001'
  _TENSORPROTO.fields_by_name['uint64_data']._options = None
  _TENSORPROTO.fields_by_name['uint64_data']._serialized_options = b'\020\001'
  _VERSION._serialized_start=4577
  _VERSION._serialized_end=4856
  _OPERATORSTATUS._serialized_start=4858
  _OPERATORSTATUS._serialized_end=4904
  _ATTRIBUTEPROTO._serialized_start=29
  _ATTRIBUTEPROTO._serialized_end=760
  _ATTRIBUTEPROTO_ATTRIBUTETYPE._serialized_start=528
  _ATTRIBUTEPROTO_ATTRIBUTETYPE._serialized_end=745
  _VALUEINFOPROTO._serialized_start=763
  _VALUEINFOPROTO._serialized_end=898
  _NODEPROTO._serialized_start=901
  _NODEPROTO._serialized_end=1123
  _TRAININGINFOPROTO._serialized_start=1126
  _TRAININGINFOPROTO._serialized_end=1340
  _MODELPROTO._serialized_start=1343
  _MODELPROTO._serialized_end=1706
  _STRINGSTRINGENTRYPROTO._serialized_start=1708
  _STRINGSTRINGENTRYPROTO._serialized_end=1760
  _TENSORANNOTATION._serialized_start=1762
  _TENSORANNOTATION._serialized_end=1869
  _GRAPHPROTO._serialized_start=1872
  _GRAPHPROTO._serialized_end=2340
  _TENSORPROTO._serialized_start=2343
  _TENSORPROTO._serialized_end=3188
  _TENSORPROTO_SEGMENT._serialized_start=2792
  _TENSORPROTO_SEGMENT._serialized_end=2829
  _TENSORPROTO_DATATYPE._serialized_start=2832
  _TENSORPROTO_DATATYPE._serialized_end=3145
  _TENSORPROTO_DATALOCATION._serialized_start=3147
  _TENSORPROTO_DATALOCATION._serialized_end=3188
  _SPARSETENSORPROTO._serialized_start=3190
  _SPARSETENSORPROTO._serialized_end=3294
  _TENSORSHAPEPROTO._serialized_start=3297
  _TENSORSHAPEPROTO._serialized_end=3446
  _TENSORSHAPEPROTO_DIMENSION._serialized_start=3364
  _TENSORSHAPEPROTO_DIMENSION._serialized_end=3446
  _TYPEPROTO._serialized_start=3449
  _TYPEPROTO._serialized_end=4126
  _TYPEPROTO_TENSOR._serialized_start=3779
  _TYPEPROTO_TENSOR._serialized_end=3845
  _TYPEPROTO_SEQUENCE._serialized_start=3847
  _TYPEPROTO_SEQUENCE._serialized_end=3893
  _TYPEPROTO_MAP._serialized_start=3895
  _TYPEPROTO_MAP._serialized_end=3955
  _TYPEPROTO_OPTIONAL._serialized_start=3957
  _TYPEPROTO_OPTIONAL._serialized_end=4003
  _TYPEPROTO_SPARSETENSOR._serialized_start=4005
  _TYPEPROTO_SPARSETENSOR._serialized_end=4077
  _TYPEPROTO_OPAQUE._serialized_start=4079
  _TYPEPROTO_OPAQUE._serialized_end=4117
  _OPERATORSETIDPROTO._serialized_start=4128
  _OPERATORSETIDPROTO._serialized_end=4181
  _FUNCTIONPROTO._serialized_start=4184
  _FUNCTIONPROTO._serialized_end=4574
# @@protoc_insertion_point(module_scope)
