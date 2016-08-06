
#include <iostream>
#include <fstream>
#include <Python.h>

//this define can avoid some logs which you don't need to care about.
#define LOGGER_LEVEL LL_WARN 

#include "simhash/Simhasher.hpp"
using namespace simhash;

Simhasher simhasher("../dict/jieba.dict.utf8", "../dict/hmm_model.utf8", "../dict/idf.utf8", "../dict/stop_words.utf8");

static PyObject * _getSimhash(PyObject *self, PyObject *args)
{
    const char* c;
    if (!PyArg_ParseTuple(args, "s", &c))
        return NULL;
    //Simhasher simhasher("../dict/jieba.dict.utf8", "../dict/hmm_model.utf8", "../dict/idf.utf8", "../dict/stop_words.utf8");
    string str(c);
    size_t topN = 5;
    uint64_t u64 = 0;
    vector<pair<string ,double> > res;
    simhasher.extract(str, res, topN);
    simhasher.make(str, topN, u64);
    return PyLong_FromUnsignedLong(u64);
}

static PyObject * _isEqual(PyObject *self, PyObject *args)
{
    long long u1,u2;
    if (!PyArg_ParseTuple(args, "kk", &u1,&u2))
        return NULL;
    int res=Simhasher::isEqual((uint64_t)u1,(uint64_t)u2);
    return PyInt_FromLong(res);
}

static PyMethodDef GreateModuleMethods[] = {
    {
        "getSimhash",
        _getSimhash,
        METH_VARARGS,
        ""
    },
    {
        "isEqual",
        _isEqual,
        METH_VARARGS,
        ""
    },
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initgetSimhash(void) {
    (void) Py_InitModule("getSimhash", GreateModuleMethods);
}

PyMODINIT_FUNC initisEqual(void) {
    (void) Py_InitModule("isEqual", GreateModuleMethods);
}
