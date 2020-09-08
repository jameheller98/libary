from sqlalchemy import extract

from app.models import *


def read_book_infos(tenSach=None, theLoai=None, tacGia=None, tinhTrang = None):
    thongtinsach = ThongTinSach.query.all()

    if tenSach:
        thongtinsach = filter(lambda tt: tt.tenSach == tenSach, thongtinsach)

    if theLoai:
        thongtinsach = filter(lambda tt: tt.theLoai.value == theLoai, thongtinsach)

    if tacGia:
        thongtinsach = filter(lambda tt: tt.tacGia == tacGia, thongtinsach)

    if tinhTrang:
        thongtinsach =  filter(lambda tt: tt.tinhTrangSach.value == tinhTrang, thongtinsach)

    return thongtinsach


def theLoaiA(thang=0):
    thongKeLuotMuon = PhieuMuonSach.query.filter(extract('month', PhieuMuonSach.ngayMuon) == thang).all()

    thongKeLuotMuonA = list(filter(lambda tk: tk.thongtinsach.theLoai == TheLoaiSach.A, thongKeLuotMuon))

    return thongKeLuotMuonA


def theLoaiB(thang=0):
    thongKeLuotMuon = PhieuMuonSach.query.filter(extract('month', PhieuMuonSach.ngayMuon) == thang).all()

    thongKeLuotMuonB = list(filter(lambda tk: tk.thongtinsach.theLoai == TheLoaiSach.B, thongKeLuotMuon))

    return thongKeLuotMuonB


def theLoaiC(thang=0):
    thongKeLuotMuon = PhieuMuonSach.query.filter(extract('month', PhieuMuonSach.ngayMuon) == thang).all()

    thongKeLuotMuonC = list(filter(lambda tk: tk.thongtinsach.theLoai == TheLoaiSach.C, thongKeLuotMuon))

    return thongKeLuotMuonC


def sachTraTre(thang=0):
    thongKeTraTre = PhieuTraSach.query.filter(extract('month', PhieuTraSach.ngayTra) == thang).all()

    thongKeTraTre = list(filter(lambda tk: tk.tienPhatKiNay != 0, thongKeTraTre))

    return thongKeTraTre


def docGiaNoTien():
    thongKeNoTien = TheDocGia.query.all()

    thongKeNoTien = list(filter(lambda tk: tk.tongNo !=0, thongKeNoTien))

    return thongKeNoTien


if __name__ == "__main__":
    print(read_book_infos())