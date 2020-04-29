# import mpi4py

from mpi4py import MPI

# buat COMM
comm = MPI.COMM_WORLD

# dapatkan rank proses
rank = comm.Get_rank()


# dapatkan total proses berjalan
size = comm.Get_size()


# jika saya rank ke 0 maka saya akan mengirimkan pesan ke proses yang mempunyai rank 1 s.d size
if rank ==0:
    data = {'A' : ('bismillahirrohmanirrohim', 'semoga'),
            'B' : ('Corona', 'Segera', 'Berlalu')}
	
# jika saya bukan rank 0 maka saya menerima pesan
else:
    data = None

data = comm.bcast(data, root=0)
print('rank ', rank, data)
