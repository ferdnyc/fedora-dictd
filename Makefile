# Makefile for source rpm: dictd
# $Id$
NAME := dictd
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
