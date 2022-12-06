import numpy as np
import pyopencl as cl
import os, sys

MAX_CHUNK_SIZE = 101

#gets all files in the current directory and then makes a list of any .exes
def get_payloads():
    payloads = []
    for x in os.listdir(os.getcwd()):
        if x[-3:] == "exe":
            payloads.append(x)
    return payloads
    
#reads any given files in binary
def read_binary(x):
    for file in x:
        payload = open(file, "rb")
        size=payload.seek(0, os.SEEK_END)
        result = []
        y=0
        while (y < size):
            payload.seek(y)
            result.append(payload.read(1))
            y+=1
        payload.close()
        return result

#reads any given files in binary
def read_binary_bad(x):
    for file in x:
        result = open(file, "rb")
        print(result.readline())

#Gets any and all opencl platforms with available GPUs in a list
def getFirstAvailableGPU():
    platforms = cl.get_platforms()
    available_platforms = []
    for x in platforms:
        for y in x.get_devices(device_type=cl.device_type.GPU):
            available_platforms.append(x)
    return platforms

platforms = getFirstAvailableGPU()
#context with the first available gpu in the platforms list
context = cl.Context(devices=[platforms[0].get_devices(device_type=cl.device_type.GPU)[0]])
queue = cl.CommandQueue(context)

program = cl.Program(context, """
#define MAX_LOAD_SIZE 101

__kernel void _in(
__global uchar *src, __global uchar *res
) {
    int gid = get_global_id(0);
    
    res[gid] = src[gid] + 1;
}
""").build()

#make a list of byte lists so that the program can iterate through each one and format it in the correct matter for the cl program
def chunkPayload():
    pass

#result = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, )
def main():
    a = np.array([1])
    print("The input array: ", a)
    src = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, a.nbytes, a)
    res = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, a.nbytes)
    kernel = program._in
    kernel.set_args(src, res)

    out = np.empty(a.shape, a.dtype)
    print("The output array before copying the data: ", out)
    cl.enqueue_copy(queue, out, res)
    cl._enqueue_read_buffer(queue, res, out)
    print("The output array after copying the data: ", out)
    #res_np = np.empty_like(a_np)
    
    #cl.enqueue_copy(queue, res_np, res)
    #print(res_np)
main()
