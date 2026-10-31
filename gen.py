import sys, os, uuid, shutil, zipfile
from data_cs import ITEMS
from data_b import ITEMS_B

mssv = sys.argv[1] if len(sys.argv) > 1 else "MSSV"
hoten = sys.argv[2] if len(sys.argv) > 2 else "HoTen"
sol_name = f"{mssv}_{hoten}_DesignPattern"
out = os.path.join(sys.argv[3] if len(sys.argv) > 3 else ".", sol_name)
if os.path.exists(out): shutil.rmtree(out)
os.makedirs(out)

ALL = ITEMS + ITEMS_B
assert len(ALL) == 23, len(ALL)

CSPROJ = """<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>disable</Nullable>
    <LangVersion>latest</LangVersion>
  </PropertyGroup>

</Project>
"""
def g(name): return "{" + str(uuid.uuid5(uuid.NAMESPACE_DNS, name)).upper() + "}"
CS, FOLDER = "{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}", "{2150E333-8FDC-42A3-9474-1A3956D46DE8}"

projects = []  # (name, guid, parentFolderGuid)
cats = ["Creational", "Structural", "Behavioral"]
folders = []   # (name, guid, parent)
for i, c in enumerate(cats, 1):
    folders.append((f"{i}_{c}", g("cat" + c), None))
    folders.append(("Pattern", g("pat" + c), g("cat" + c)))
    folders.append(("Real", g("real" + c), g("cat" + c)))

def write(name, code):
    d = os.path.join(out, name); os.makedirs(d)
    open(os.path.join(d, f"{name}.csproj"), "w", encoding="utf-8").write(CSPROJ)
    open(os.path.join(d, "Program.cs"), "w", encoding="utf-8-sig").write(code.lstrip("\n"))

for cat, pat, real, code_pat, code_real in ALL:
    n1 = f"{mssv}_{pat}Pattern"
    n2 = f"{mssv}_{pat}_{real}"
    write(n1, code_pat); write(n2, code_real)
    projects.append((n1, g(n1), g("pat" + cat)))
    projects.append((n2, g(n2), g("real" + cat)))
assert len(projects) == 46

L = ["", "Microsoft Visual Studio Solution File, Format Version 12.00", "# Visual Studio Version 17",
     "VisualStudioVersion = 17.0.31903.59", "MinimumVisualStudioVersion = 10.0.40219.1"]
for n, gu, _ in folders:
    L += [f'Project("{FOLDER}") = "{n}", "{n}", "{gu}"', "EndProject"]
for n, gu, _ in projects:
    L += [f'Project("{CS}") = "{n}", "{n}\\{n}.csproj", "{gu}"', "EndProject"]
L += ["Global", "\tGlobalSection(SolutionConfigurationPlatforms) = preSolution",
      "\t\tDebug|Any CPU = Debug|Any CPU", "\t\tRelease|Any CPU = Release|Any CPU", "\tEndGlobalSection",
      "\tGlobalSection(ProjectConfigurationPlatforms) = postSolution"]
for _, gu, _ in projects:
    for cfg in ("Debug", "Release"):
        L += [f"\t\t{gu}.{cfg}|Any CPU.ActiveCfg = {cfg}|Any CPU", f"\t\t{gu}.{cfg}|Any CPU.Build.0 = {cfg}|Any CPU"]
L += ["\tEndGlobalSection", "\tGlobalSection(SolutionProperties) = preSolution", "\t\tHideSolutionNode = FALSE",
      "\tEndGlobalSection", "\tGlobalSection(NestedProjects) = preSolution"]
for _, gu, p in folders:
    if p: L.append(f"\t\t{gu} = {p}")
for _, gu, p in projects:
    L.append(f"\t\t{gu} = {p}")
L += ["\tEndGlobalSection", "EndGlobal", ""]
open(os.path.join(out, sol_name + ".sln"), "w", encoding="utf-8-sig", newline="").write("\r\n".join(L))

open(os.path.join(out, ".gitignore"), "w").write("bin/\nobj/\n.vs/\n*.user\n")

rows = []
for i, (cat, pat, real, *_ ) in enumerate(ALL, 1):
    rows.append(f"| {i} | {cat} | {pat} | `{mssv}_{pat}Pattern` | `{mssv}_{pat}_{real}` |")
readme = f"""# {sol_name}

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
""" + "\n".join(rows) + "\n"
open(os.path.join(out, "README.md"), "w", encoding="utf-8").write(readme)
shutil.copy(__file__, os.path.join(out, "gen.py"))
shutil.copy("data_cs.py", out); shutil.copy("data_b.py", out)
print(sol_name, len(projects))
