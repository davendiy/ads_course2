
import os
import datetime
import tarfile

CHUNK = 1024 * 500


def copyfile(filename, fromdir, todir):
    fromfullpath = os.path.join(fromdir, filename)  # РїРѕРІРЅРёР№ С€Р»СЏС… РґРѕ РІРёС…С–РґРЅРѕРіРѕ С„Р°Р№Р»Сѓ
    tofullpath = os.path.join(todir, filename)  # РїРѕРІРЅРёР№ С€Р»СЏС… РґРѕ С„Р°Р№Р»Сѓ СЂРµР·СѓР»СЊС‚Р°С‚Сѓ
    fromfile = open(fromfullpath, "rb")
    tofile = open(tofullpath, "wb")
    if os.path.getsize(fromfullpath) <= CHUNK:  # СЏРєС‰Рѕ С„Р°Р№Р» РЅРµРІРµР»РёРєРёР№
        cnt = fromfile.read()  # С‡РёС‚Р°С”РјРѕ Р·Р° РѕРґРёРЅ СЂР°Р·
        tofile.write(cnt)
    else:
        while True:
            cnt = fromfile.read(CHUNK)  # С–РЅР°РєС€Рµ С‡РёС‚Р°С”РјРѕ РїРѕ С‡Р°СЃС‚РёРЅР°С…
            if not cnt: break
            tofile.write(cnt)
    fromfile.close()
    tofile.close()


def copydir(fromdir, toparent):
    fromdir = os.path.normpath(fromdir)  # РѕС‚СЂРёРјСѓС”РјРѕ РїРѕРІРЅС– С€Р»СЏС…Рё РґРѕ РєР°С‚Р°Р»РѕРіС–РІ
    toparent = os.path.normpath(toparent)
    last = os.path.split(fromdir)[-1]  # last - РѕСЃС‚Р°РЅРЅСЏ С‡Р°СЃС‚РёРЅР° С€Р»СЏС…Сѓ - С–Рј'СЏ РєР°С‚Р»РѕРіСѓ
    curdir = os.path.join(toparent, last)
    print(curdir)
    os.mkdir(curdir)  # СЃС‚РІРѕСЂСЋС”РјРѕ РїС–РґРєР°С‚Р»РѕРі Сѓ СЂРµР·СѓР»СЊС‚СѓСЋС‡РѕРјСѓ РєР°С‚Р°Р»РѕР·С–
    lst = os.listdir(fromdir)  # РѕС‚СЂРёРјСѓС”РјРѕ РІРјС–СЃС‚ РІРёС…С–РґРЅРѕРіРѕ РєР°С‚Р°Р»РѕРіСѓ
    for item in lst:
        fullitem = os.path.join(fromdir, item)  # РїРѕРІРЅРёР№ С€Р»СЏС… РґРѕ РµР»РµРјРµРЅС‚Сѓ РєР°С‚Р°Р»РѕРіСѓ
        if os.path.isfile(fullitem):  # СЏРєС‰Рѕ С„Р°Р№Р» С‚Рѕ РєРѕРїС–СЋС”РјРѕ Р№РѕРіРѕ
            try:
                copyfile(item, fromdir, curdir)
            except Exception as e:
                print('copydir: skipping', item, e)  # РїСЂРѕРїСѓСЃРєР°С”РјРѕ С„Р°Р№Р», СЏРєС‰Рѕ РїРѕРјРёР»РєР°
        else:
            copydir(fullitem,
                    curdir)  # СЏРєС‰Рѕ РєР°С‚Р°Р»РѕРі, С‚Рѕ СЂРµРєСѓСЂСЃРёРІРЅРѕ РІРёРєР»РёРєР°С”РјРѕ СЃРµР±Рµ


def getbackupname(backupdir):
    dt = datetime.datetime.now()
    dirname = dt.strftime('%Y%m%d_%H%M%S')  # С„РѕСЂРјСѓС”РјРѕ С–Рј'СЏ РєР°С‚Р°Р»РѕРіСѓ Р·Р° РїРѕС‚РѕС‡РЅРёРј С‡Р°СЃРѕРј
    return os.path.join(backupdir, dirname)


def removedir(dir):
    dir = os.path.normpath(dir)  # РѕС‚СЂРёРјСѓС”РјРѕ РїРѕРІРЅРёР№ С€Р»СЏС… С€Р»СЏС…Рё РґРѕ РєР°С‚Р°Р»РѕРіСѓ
    lst = os.listdir(dir)  # РѕС‚СЂРёРјСѓС”РјРѕ РІРјС–СЃС‚ РєР°С‚Р°Р»РѕРіСѓ
    for item in lst:
        fullitem = os.path.join(dir, item)  # РїРѕРІРЅРёР№ С€Р»СЏС… РґРѕ РµР»РµРјРµРЅС‚Сѓ РєР°С‚Р°Р»РѕРіСѓ
        if os.path.isfile(fullitem):  # СЏРєС‰Рѕ С„Р°Р№Р» С‚Рѕ РІРёРґР°Р»СЏС”РјРѕ Р№РѕРіРѕ
            try:
                os.remove(fullitem)
            except Exception as e:
                print('removedir: skipping', item, e)  # РїСЂРѕРїСѓСЃРєР°С”РјРѕ С„Р°Р№Р», СЏРєС‰Рѕ РїРѕРјРёР»РєР°
        else:
            removedir(fullitem)  # СЏРєС‰Рѕ РєР°С‚Р°Р»РѕРі, С‚Рѕ СЂРµРєСѓСЂСЃРёРІРЅРѕ РІРёРєР»РёРєР°С”РјРѕ СЃРµР±Рµ
    os.rmdir(dir)  # РІРёРґР°Р»СЏС”РјРѕ РїРѕСЂРѕР¶РЅС–Р№ РєР°С‚Р°Р»РѕРі


def archivesubdirs(dir):
    lst = os.listdir(dir)  # РѕС‚СЂРёРјСѓС”РјРѕ РІРјС–СЃС‚ РєР°С‚Р°Р»РѕРіСѓ
    for item in lst:
        fullitem = os.path.join(dir, item)  # РїРѕРІРЅРёР№ С€Р»СЏС… РґРѕ РµР»РµРјРµРЅС‚Сѓ РєР°С‚Р°Р»РѕРіСѓ
        if os.path.isdir(fullitem):  # СЏРєС‰Рѕ РєР°С‚Р°Р»РѕРі С‚Рѕ Р°СЂС…С–РІСѓС”РјРѕ Р№РѕРіРѕ
            try:
                tf = tarfile.open(fullitem + '.tar.gz', 'w:gz')
                tf.add(fullitem)
                tf.close()
                removedir(fullitem)  # РІРёРґР°Р»СЏС”РјРѕ Р·Р°Р°СЂС…С–РІРѕРІР°РЅРёР№ РїС–РґРєР°С‚Р°Р»РѕРі
            except Exception as e:
                print('archivesubdirs: skipping', item,
                      e)  # РїСЂРѕРїСѓСЃРєР°С”РјРѕ РїС–РґРєР°С‚Р°Р»РѕРі, СЏРєС‰Рѕ РїРѕРјРёР»РєР°


def backupdirectories(directories, backupdir):
    archivesubdirs(backupdir)  # Р°СЂС…С–РІСѓС”РјРѕ РїРѕРїРµСЂРµРґРЅС– РІРµСЂСЃС–С—
    toparent = getbackupname(backupdir)
    #    print(toparent)
    os.mkdir(toparent)
    for dir in directories:
        try:
            copydir(dir, toparent)
        except Exception as e:
            print('backupdirectories: skipping', dir,
                  e)  # РїСЂРѕРїСѓСЃРєР°С”РјРѕ РєР°С‚Р°Р»РѕРі, СЏРєС‰Рѕ РїРѕРјРёР»РєР°


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:  # СЏРєС‰Рѕ РЅРµ РІРёСЃС‚Р°С‡Р°С” РїР°СЂР°РјРµС‚СЂС–РІ, РІРІРµСЃС‚Рё
        backupdir = input("Backup directory: ")
        directories = input("Directories to backup: ").split()
    else:
        backupdir = sys.argv[1]  # 1 РїР°СЂР°РјРµС‚СЂ
        directories = sys.argv[2:]  # РїР°СЂР°РјРµС‚СЂРё, РїРѕС‡РёРЅР°СЋС‡Рё Р· 2
    backupdirectories(directories, backupdir)

