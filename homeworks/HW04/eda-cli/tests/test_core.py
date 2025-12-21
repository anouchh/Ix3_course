from __future__ import annotations

import pandas as pd

from eda_cli.core import (
    compute_quality_flags,
    correlation_matrix,
    flatten_summary_for_print,
    missing_table,
    summarize_dataset,
    top_categories,
)


def _sample_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "age": [10, 20, 30, None],
            "height": [140, 150, 160, 170],
            "city": ["A", "B", "A", None],
        }
    )


def test_summarize_dataset_basic():
    df = _sample_df()
    summary = summarize_dataset(df)

    assert summary.n_rows == 4
    assert summary.n_cols == 3
    assert any(c.name == "age" for c in summary.columns)
    assert any(c.name == "city" for c in summary.columns)

    summary_df = flatten_summary_for_print(summary)
    assert "name" in summary_df.columns
    assert "missing_share" in summary_df.columns


def test_missing_table_and_quality_flags():
    df = _sample_df()
    missing_df = missing_table(df)

    assert "missing_count" in missing_df.columns
    assert missing_df.loc["age", "missing_count"] == 1

    summary = summarize_dataset(df)
    flags = compute_quality_flags(df, summary, missing_df)
    assert 0.0 <= flags["quality_score"] <= 1.0


def test_correlation_and_top_categories():
    df = _sample_df()
    corr = correlation_matrix(df)
    # корреляция между age и height существует
    assert "age" in corr.columns or corr.empty is False

    top_cats = top_categories(df, max_columns=5, top_k=2)
    assert "city" in top_cats
    city_table = top_cats["city"]
    assert "value" in city_table.columns
    assert len(city_table) <= 2

def test_constant_columns_heuristic():
    """Тестируем обнаружение постоянных колонок"""
    # 1. DataFrame с постоянной колонкой
    df_with_constant = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', 'Bob', 'Charlie', 'David'],
        'status': ['active', 'active', 'active', 'active'],  # постоянная!
        'value': [10, 20, 30, 40]
    })
    
    summary = summarize_dataset(df_with_constant)
    missing_df = missing_table(df_with_constant)
    flags = compute_quality_flags(df_with_constant, summary, missing_df)
    
    # Проверяем, что флаг установлен в True
    assert flags['has_constant_columns'] == True
    assert flags['constant_columns_count'] == 1
    assert 'status' in flags['constant_columns_list']
    
    # 2. DataFrame без постоянных колонок
    df_without_constant = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['A', 'B', 'C', 'D'],
        'value': [10, 20, 10, 20]  # есть повторения, но не постоянная
    })
    
    summary2 = summarize_dataset(df_without_constant)
    missing_df2 = missing_table(df_without_constant)
    flags2 = compute_quality_flags(df_without_constant, summary2, missing_df2)
    
    assert flags2['has_constant_columns'] == False
    assert flags2['constant_columns_count'] == 0


def test_suspicious_id_duplicates_heuristic():
    """Тестируем обнаружение дубликатов ID"""
    # 1. DataFrame с дубликатами ID
    df_with_duplicates = pd.DataFrame({
        'user_id': [101, 102, 103, 101, 105],  # дубликат 101!
        'transaction_id': ['tx1', 'tx2', 'tx3', 'tx4', 'tx5'],
        'value': [100, 200, 300, 400, 500]
    })
    
    summary = summarize_dataset(df_with_duplicates)
    missing_df = missing_table(df_with_duplicates)
    flags = compute_quality_flags(df_with_duplicates, summary, missing_df)
    
    assert flags['has_suspicious_id_duplicates'] == True
    assert 'user_id' in flags['suspicious_duplicates_dict']
    
    # Проверяем детали дубликатов
    dup_info = flags['suspicious_duplicates_dict']['user_id']
    assert dup_info['duplicate_count'] == 1  # один дубликат
    assert dup_info['duplicate_share'] == 0.2  # 1/5 = 20%
    
    # 2. DataFrame без дубликатов ID
    df_without_duplicates = pd.DataFrame({
        'id': [1, 2, 3, 4, 5],
        'uuid': ['a', 'b', 'c', 'd', 'e'],
        'value': [10, 20, 30, 40, 50]
    })
    
    summary2 = summarize_dataset(df_without_duplicates)
    missing_df2 = missing_table(df_without_duplicates)
    flags2 = compute_quality_flags(df_without_duplicates, summary2, missing_df2)
    
    assert flags2['has_suspicious_id_duplicates'] == False


def test_quality_score_with_new_heuristics():
    """Тестируем, что quality_score учитывает новые эвристики"""
    # Идеальные данные (должен быть высокий score)
    df_good = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['A', 'B', 'C', 'D'],
        'value': [10, 20, 30, 40]
    })
    
    # Проблемные данные (должен быть низкий score)
    df_bad = pd.DataFrame({
        'user_id': [1, 2, 1, 3],  # дубликаты
        'status': ['X', 'X', 'X', 'X'],  # постоянная колонка
        'value': [10, None, 30, 40]  # пропуск
    })
    
    summary_good = summarize_dataset(df_good)
    missing_good = missing_table(df_good)
    flags_good = compute_quality_flags(df_good, summary_good, missing_good)
    
    summary_bad = summarize_dataset(df_bad)
    missing_bad = missing_table(df_bad)
    flags_bad = compute_quality_flags(df_bad, summary_bad, missing_bad)
    
    # Score хороших данных должен быть выше
    assert flags_good['quality_score'] > flags_bad['quality_score']
    
    # Проверяем, что score в диапазоне 0-1
    assert 0.0 <= flags_good['quality_score'] <= 1.0
    assert 0.0 <= flags_bad['quality_score'] <= 1.0


def test_all_flags_present():
    """Проверяем, что все ожидаемые флаги присутствуют в результатах"""
    df = pd.DataFrame({
        'id': [1, 2, 3],
        'value': [10, 20, 30]
    })
    
    summary = summarize_dataset(df)
    missing_df = missing_table(df)
    flags = compute_quality_flags(df, summary, missing_df)
    
    # Базовые флаги
    expected_flags = [
        'too_few_rows',
        'too_many_columns',
        'max_missing_share',
        'too_many_missing',
        'quality_score'
    ]
    
    # Новые флаги
    new_flags = [
        'has_constant_columns',
        'constant_columns_list',
        'constant_columns_count',
        'has_suspicious_id_duplicates',
        'suspicious_duplicates_dict'
    ]
    
    # Проверяем все флаги
    for flag in expected_flags + new_flags:
        assert flag in flags, f"Флаг '{flag}' отсутствует в результатах"