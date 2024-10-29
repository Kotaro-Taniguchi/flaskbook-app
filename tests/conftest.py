import os
import shutil

import pytest

from apps.app import create_app, db

from apps.crud.models import User
from apps.detector.models import UserImage, UserImageTag


@pytest.fixture
def app_data():
    return 3


@pytest.fixture
def fixture_app():
    # テスト用のコンフィグを使う
    app = create_app("testing")

    # データベースを利用するための宣言
    app.app_context().push()

    # テスト用データベースのテーブルを作成
    with app.app_context():
        db.create_all()

    # テスト用の画像アップロードディレクトリを作成
    os.mkdir(app.config["UPLOAD_FOLDER"])

    # テストを実行
    yield app

    # クリーンナップ処理
    # userテーブルのレコードを削除
    User.query.delete()

    UserImage.query.delete()

    UserImageTag.query.delete()

    # 画像アップロードディレクトリを削除
    shutil.rmtree(app.config["UPLOAD_FOLDER"])

    db.session.commit()


# Flaskのテストクライアントを返すフィクスチャ関数
@pytest.fixture
def client(fixture_app):
    return fixture_app.test_client()
