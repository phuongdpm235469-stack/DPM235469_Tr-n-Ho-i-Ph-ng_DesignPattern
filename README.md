# MSSV_HoTen_DesignPattern

Solution gồm **46 project** (23 mẫu GoF x 2): mỗi mẫu có
- **Pattern**: ví dụ mẫu chuẩn (theo refactoring.guru)
- **Real**: ứng dụng mẫu vào phần mềm **Quản lý bán hàng**

Cấu trúc: Creational (5) · Structural (7) · Behavioral (11).

## Chạy
Yêu cầu .NET 8 SDK. Mở file `.sln` bằng Visual Studio 2022, chuột phải project > *Set as Startup Project* > Ctrl+F5.
Hoặc: `dotnet run --project <ten_project>`

## Đổi MSSV / Họ tên
`python gen.py <MSSV> <HoTen>` (tạo lại toàn bộ solution với tên mới).

| # | Nhóm | Mẫu | Project Pattern | Project Real |
|---|------|-----|-----------------|--------------|
| 1 | Creational | Singleton | `MSSV_SingletonPattern` | `MSSV_Singleton_QuanLyPhienPOS` |
| 2 | Creational | Builder | `MSSV_BuilderPattern` | `MSSV_Builder_KhoiTaoDonHang` |
| 3 | Creational | Prototype | `MSSV_PrototypePattern` | `MSSV_Prototype_NhanBanDonHang` |
| 4 | Creational | FactoryMethod | `MSSV_FactoryMethodPattern` | `MSSV_FactoryMethod_CongThanhToan` |
| 5 | Creational | AbstractFactory | `MSSV_AbstractFactoryPattern` | `MSSV_AbstractFactory_ChungTuDaKenh` |
| 6 | Structural | Adapter | `MSSV_AdapterPattern` | `MSSV_Adapter_CongVanChuyen` |
| 7 | Structural | Bridge | `MSSV_BridgePattern` | `MSSV_Bridge_NenTangThietBi` |
| 8 | Structural | Composite | `MSSV_CompositePattern` | `MSSV_Composite_LuongNhanVien` |
| 9 | Structural | Decorator | `MSSV_DecoratorPattern` | `MSSV_Decorator_TinhHoaDonDong` |
| 10 | Structural | Facade | `MSSV_FacadePattern` | `MSSV_Facade_DatHangMotCham` |
| 11 | Structural | Flyweight | `MSSV_FlyweightPattern` | `MSSV_Flyweight_ToiUuBoNhoSanPham` |
| 12 | Structural | Proxy | `MSSV_ProxyPattern` | `MSSV_Proxy_DemDanhMucSanPham` |
| 13 | Behavioral | ChainOfResponsibility | `MSSV_ChainOfResponsibilityPattern` | `MSSV_ChainOfResponsibility_DuyetGiamGia` |
| 14 | Behavioral | Command | `MSSV_CommandPattern` | `MSSV_Command_ThaoTacGioHang` |
| 15 | Behavioral | Iterator | `MSSV_IteratorPattern` | `MSSV_Iterator_LichSuDonHang` |
| 16 | Behavioral | Mediator | `MSSV_MediatorPattern` | `MSSV_Mediator_ManHinhBanHang` |
| 17 | Behavioral | Memento | `MSSV_MementoPattern` | `MSSV_Memento_HoanTacGioHang` |
| 18 | Behavioral | Observer | `MSSV_ObserverPattern` | `MSSV_Observer_CanhBaoTonKho` |
| 19 | Behavioral | State | `MSSV_StatePattern` | `MSSV_State_TrangThaiDonHang` |
| 20 | Behavioral | Strategy | `MSSV_StrategyPattern` | `MSSV_Strategy_ChinhSachGiamGia` |
| 21 | Behavioral | TemplateMethod | `MSSV_TemplateMethodPattern` | `MSSV_TemplateMethod_QuyTrinhXuLyDon` |
| 22 | Behavioral | Visitor | `MSSV_VisitorPattern` | `MSSV_Visitor_TinhThueTheoLoaiHang` |
| 23 | Behavioral | Interpreter | `MSSV_InterpreterPattern` | `MSSV_Interpreter_QuyTacCoupon` |
