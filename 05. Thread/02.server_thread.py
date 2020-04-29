# import socket, sys, traceback dan threading
import socket, sys, traceback, threading

# jalankan server
def main():
    start_server()

# fungsi saat server dijalankan
def start_server():
    # tentukan IP server
    ip = "127.0.0.1"
    
    # tentukan port server
    port = 8080

    # buat socket bertipe TCP
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # option socket
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket dibuat")

    # lakukan bind
    try:
        soc.bind((ip, port))
    except:
        # exit pada saat error
        print("Bind gagal. Error : " + str(sys.exc_info()))
        sys.exit()

    # listen hingga 5 antrian
    soc.listen(5)
    print("Socket mendengarkan")

    # infinite loop, jangan reset setiap ada request
    while True:
        # terima koneksi
        conn, addr = soc.accept()
        
        # dapatkan IP dan port
        ip = addr[0]
        port = addr[1]
        print("Connected dengan " + str(ip) + ":" + str(port))

        # jalankan thread untuk setiap koneksi yang terhubung
        try:
            tred = client_thread(conn, ip, port)
            tred.start()
        except:
            # print kesalahan jika thread tidak berhasil dijalankan
            print("Thread tidak berjalan.")
            traceback.print_exc()

    # tutup socket
    soc.close()


def client_thread(connection, ip, port, max_buffer_size = 4096):
    # flag koneksi
    flag = True

    # selama koneksi aktif
    while connection:

        # terima pesan dari client
        msg = " "
        client_input = connection.recv(max_buffer_size)
        
        # dapatkan ukuran pesan
        client_input_size = len(client_input)
        
        # print jika pesan terlalu besar
        if client_input_size > max_buffer_size:
            print("The input size is greater than expected {}")

        # dapatkan pesan setelah didecode
        client_input = client_input.decode()
        
        # jika "quit" maka flag koneksi = false, matikan koneksi
        if "quit" in client_input:
            # ubah flag
            flag = False
            print("Client meminta keluar")
            
            # matikan koneksi
            connection.close()
            print("Connection " + str(ip) + ":" + str(port) + " ditutup")
            
        else:
            # tampilkan pesan dari client
            print("Pesan dari client : ", client_input)
            
            
# panggil fungsi utama
if __name__ == "__main__":
    main()