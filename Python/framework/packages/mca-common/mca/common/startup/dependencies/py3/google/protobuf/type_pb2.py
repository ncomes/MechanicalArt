# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/protobuf/type.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import source_context_pb2 as google_dot_protobuf_dot_source__context__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1agoogle/protobuf/type.proto\x12\x0fgoogle.protobuf\x1a\x19google/protobuf/any.proto\x1a$google/protobuf/source_context.proto\"\xa7\x02\n\x04Type\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12.\n\x06\x66ields\x18\x02 \x03(\x0b\x32\x16.google.protobuf.FieldR\x06\x66ields\x12\x16\n\x06oneofs\x18\x03 \x03(\tR\x06oneofs\x12\x31\n\x07options\x18\x04 \x03(\x0b\x32\x17.google.protobuf.OptionR\x07options\x12\x45\n\x0esource_context\x18\x05 \x01(\x0b\x32\x1e.google.protobuf.SourceContextR\rsourceContext\x12/\n\x06syntax\x18\x06 \x01(\x0e\x32\x17.google.protobuf.SyntaxR\x06syntax\x12\x18\n\x07\x65\x64ition\x18\x07 \x01(\tR\x07\x65\x64ition\"\xb4\x06\n\x05\x46ield\x12/\n\x04kind\x18\x01 \x01(\x0e\x32\x1b.google.protobuf.Field.KindR\x04kind\x12\x44\n\x0b\x63\x61rdinality\x18\x02 \x01(\x0e\x32\".google.protobuf.Field.CardinalityR\x0b\x63\x61rdinality\x12\x16\n\x06number\x18\x03 \x01(\x05R\x06number\x12\x12\n\x04name\x18\x04 \x01(\tR\x04name\x12\x19\n\x08type_url\x18\x06 \x01(\tR\x07typeUrl\x12\x1f\n\x0boneof_index\x18\x07 \x01(\x05R\noneofIndex\x12\x16\n\x06packed\x18\x08 \x01(\x08R\x06packed\x12\x31\n\x07options\x18\t \x03(\x0b\x32\x17.google.protobuf.OptionR\x07options\x12\x1b\n\tjson_name\x18\n \x01(\tR\x08jsonName\x12#\n\rdefault_value\x18\x0b \x01(\tR\x0c\x64\x65\x66\x61ultValue\"\xc8\x02\n\x04Kind\x12\x10\n\x0cTYPE_UNKNOWN\x10\x00\x12\x0f\n\x0bTYPE_DOUBLE\x10\x01\x12\x0e\n\nTYPE_FLOAT\x10\x02\x12\x0e\n\nTYPE_INT64\x10\x03\x12\x0f\n\x0bTYPE_UINT64\x10\x04\x12\x0e\n\nTYPE_INT32\x10\x05\x12\x10\n\x0cTYPE_FIXED64\x10\x06\x12\x10\n\x0cTYPE_FIXED32\x10\x07\x12\r\n\tTYPE_BOOL\x10\x08\x12\x0f\n\x0bTYPE_STRING\x10\t\x12\x0e\n\nTYPE_GROUP\x10\n\x12\x10\n\x0cTYPE_MESSAGE\x10\x0b\x12\x0e\n\nTYPE_BYTES\x10\x0c\x12\x0f\n\x0bTYPE_UINT32\x10\r\x12\r\n\tTYPE_ENUM\x10\x0e\x12\x11\n\rTYPE_SFIXED32\x10\x0f\x12\x11\n\rTYPE_SFIXED64\x10\x10\x12\x0f\n\x0bTYPE_SINT32\x10\x11\x12\x0f\n\x0bTYPE_SINT64\x10\x12\"t\n\x0b\x43\x61rdinality\x12\x17\n\x13\x43\x41RDINALITY_UNKNOWN\x10\x00\x12\x18\n\x14\x43\x41RDINALITY_OPTIONAL\x10\x01\x12\x18\n\x14\x43\x41RDINALITY_REQUIRED\x10\x02\x12\x18\n\x14\x43\x41RDINALITY_REPEATED\x10\x03\"\x99\x02\n\x04\x45num\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x38\n\tenumvalue\x18\x02 \x03(\x0b\x32\x1a.google.protobuf.EnumValueR\tenumvalue\x12\x31\n\x07options\x18\x03 \x03(\x0b\x32\x17.google.protobuf.OptionR\x07options\x12\x45\n\x0esource_context\x18\x04 \x01(\x0b\x32\x1e.google.protobuf.SourceContextR\rsourceContext\x12/\n\x06syntax\x18\x05 \x01(\x0e\x32\x17.google.protobuf.SyntaxR\x06syntax\x12\x18\n\x07\x65\x64ition\x18\x06 \x01(\tR\x07\x65\x64ition\"j\n\tEnumValue\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\x16\n\x06number\x18\x02 \x01(\x05R\x06number\x12\x31\n\x07options\x18\x03 \x03(\x0b\x32\x17.google.protobuf.OptionR\x07options\"H\n\x06Option\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12*\n\x05value\x18\x02 \x01(\x0b\x32\x14.google.protobuf.AnyR\x05value*C\n\x06Syntax\x12\x11\n\rSYNTAX_PROTO2\x10\x00\x12\x11\n\rSYNTAX_PROTO3\x10\x01\x12\x13\n\x0fSYNTAX_EDITIONS\x10\x02\x42{\n\x13\x63om.google.protobufB\tTypeProtoP\x01Z-google.golang.org/protobuf/types/known/typepb\xf8\x01\x01\xa2\x02\x03GPB\xaa\x02\x1eGoogle.Protobuf.WellKnownTypesb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'google.protobuf.type_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\023com.google.protobufB\tTypeProtoP\001Z-google.golang.org/protobuf/types/known/typepb\370\001\001\242\002\003GPB\252\002\036Google.Protobuf.WellKnownTypes'
  _globals['_SYNTAX']._serialized_start=1699
  _globals['_SYNTAX']._serialized_end=1766
  _globals['_TYPE']._serialized_start=113
  _globals['_TYPE']._serialized_end=408
  _globals['_FIELD']._serialized_start=411
  _globals['_FIELD']._serialized_end=1231
  _globals['_FIELD_KIND']._serialized_start=785
  _globals['_FIELD_KIND']._serialized_end=1113
  _globals['_FIELD_CARDINALITY']._serialized_start=1115
  _globals['_FIELD_CARDINALITY']._serialized_end=1231
  _globals['_ENUM']._serialized_start=1234
  _globals['_ENUM']._serialized_end=1515
  _globals['_ENUMVALUE']._serialized_start=1517
  _globals['_ENUMVALUE']._serialized_end=1623
  _globals['_OPTION']._serialized_start=1625
  _globals['_OPTION']._serialized_end=1697
# @@protoc_insertion_point(module_scope)
