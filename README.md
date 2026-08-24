# inno-khorasan-petrochemical-SEM

سامانه مدیریت انرژی هوشمند پتروشیمی خراسان مبتنی بر یادگیری تقویتی
۱. مطالعه و شناخت پتروشیمی خراسان
۱-۱. مشخصات کلی شرکت
شرکت پتروشیمی خراسان (KHPC) در سال ۱۳۷۱ در بجنورد، مرکز استان خراسان شمالی تأسیس شده و فاز نخست آن در سال ۱۳۷۵ به بهره‌برداری رسیده است. این مجتمع با مساحتی بالغ بر ۲۰۴ هکتار در کیلومتر ۱۷ جاده بجنورد-شیروان واقع شده است.

محصولات اصلی:

آمونیاک (ظرفیت تولید سالانه ۳۳۰ هزار تن)

اوره پریل (ظرفیت تولید سالانه ۴۹۵ هزار تن)

کریستال ملامین (ظرفیت تولید سالانه ۲۰ هزار تن)

ازت مایع

مالکیت: شرکت سرمایه‌گذاری نفت، گاز و پتروشیمی تأمین (تاپیکو)

۱-۲. فرآیندهای تولید و مصرف انرژی
فرآیند تولید به صورت زنجیره‌ای است: خوراک گاز طبیعی وارد واحد تولید آمونیاک می‌شود، آمونیاک تولیدی به واحد اوره ارسال می‌شود و بخشی از آمونیاک و اوره به عنوان خوراک واحد تولید کریستال ملامین مصرف می‌شود.

مصارف انرژی کلیدی:

گاز طبیعی به عنوان خوراک و سوخت اصلی

برق مصرفی برای تجهیزات دوار و سیستم‌های تبرید

بخار فرآیندی در واحدهای مختلف

شاخص‌های مصرف انرژی ویژه (SEC):

واحد آمونیاک: ۶۲.۶۱ گیگاژول بر تن محصول (۵.۵٪ کمتر از استاندارد ملی)

واحد اوره: ۴.۵۲ گیگاژول بر تن محصول (۵.۹۷٪ کمتر از استاندارد ملی)

اتلاف اگزرژی در واحد آمونیاک (بر اساس مطالعه موجود):

بخش	اتلاف اگزرژی (GJ/h)
تولید گاز سنتز	۴۲
راکتور شیفت	۳۶
جداسازی CO₂	۳۱
سنتز آمونیاک	۶۹
تبرید	۱۲
متاناسیون	۲
۱-۳. انتشار گازهای گلخانه‌ای
بر اساس مطالعات انجام‌شده، بیشترین اثرات سوء زیست‌محیطی واحد آمونیاک مرتبط با سلامت انسان بوده و عمدتاً ناشی از مصرف متان، بخار و انتشارات واحد آمونیاک و گاز طبیعی است. صنعت پتروشیمی به طور کلی حدود ۱۴٪ از کل مصرف انرژی صنعتی و نزدیک به ۱.۵ گیگاتن انتشار CO₂ در سال را به خود اختصاص داده است.

۲. مستندات الزامات نرم‌افزاری (SRS)
۲-۱. هدف سیستم
طراحی، توسعه و استقرار سامانه مدیریت انرژی هوشمند (Smart Energy Management System - SEMS) مبتنی بر یادگیری تقویتی (Reinforcement Learning) جهت بهینه‌سازی پویای مصرف انرژی، کاهش انتشار گازهای گلخانه‌ای و افزایش بهره‌وری اقتصادی در مجتمع پتروشیمی خراسان.

۲-۲. محدوده سیستم
سیستم کلیه واحدهای تولیدی شامل:

واحد تولید آمونیاک

واحد تولید اوره

واحد تولید کریستال ملامین

واحد یوتیلیتی (تولید بخار، برق، آب خنک‌کننده، هوای فشرده، ازت مایع)

۲-۳. ورودی‌های سیستم (Inputs)
۲-۳-۱. داده‌های عملیاتی بلادرنگ (از SCADA و IoT)
شماره	نام داده	واحد	منبع	نرخ نمونه‌برداری
1	دمای خروجی ریفرمر اولیه	°C	SCADA	1 ثانیه
2	دمای خروجی ریفرمر ثانویه	°C	SCADA	1 ثانیه
3	فشار راکتور سنتز آمونیاک	bar	SCADA	1 ثانیه
4	دمای راکتور سنتز آمونیاک	°C	SCADA	1 ثانیه
5	دبی خوراک گاز طبیعی ورودی	Nm³/h	Flow Meter	1 ثانیه
6	دبی هواي ورودی به ریفرمر	Nm³/h	Flow Meter	1 ثانیه
7	دبی بخار ورودی به فرآیند	ton/h	Flow Meter	1 ثانیه
8	توان مصرفی کمپرسورهای اصلی	MW	Power Meter	1 ثانیه
9	توان مصرفی پمپ‌های اصلی	kW	Power Meter	1 ثانیه
10	دمای آب خنک‌کننده ورودی/خروجی	°C	Temperature Sensor	5 ثانیه
11	دبی آب خنک‌کننده سیرکوله	m³/h	Flow Meter	5 ثانیه
12	فشار بخار تولیدی یوتیلیتی	bar	Pressure Sensor	1 ثانیه
13	دمای بخار تولیدی	°C	Temperature Sensor	1 ثانیه
14	ترکیب گاز خوراک (CH₄, C₂H₆, C₃H₈, N₂, CO₂)	%	GC Analyzer	15 دقیقه
15	ترکیب گاز سنتز خروجی (H₂, N₂, CH₄, Ar)	%	GC Analyzer	15 دقیقه
16	دبی آمونیاک مایع تولیدی	ton/h	Flow Meter	1 دقیقه
17	دبی اوره تولیدی	ton/h	Flow Meter	1 دقیقه
18	دبی ملامین تولیدی	ton/h	Flow Meter	1 دقیقه
19	دمای محیط	°C	Weather Station	1 دقیقه
20	رطوبت نسبی محیط	%	Weather Station	1 دقیقه
۲-۳-۲. داده‌های اقتصادی
شماره	نام داده	واحد	منبع	نرخ به‌روزرسانی
21	قیمت گاز طبیعی خوراک	IRR/Nm³	سیستم مالی	روزانه
22	قیمت برق مصرفی	IRR/kWh	سیستم مالی	روزانه
23	قیمت فروش آمونیاک	IRR/ton	سیستم مالی	روزانه
24	قیمت فروش اوره	IRR/ton	سیستم مالی	روزانه
25	قیمت فروش ملامین	IRR/ton	سیستم مالی	روزانه
26	نرخ ارز مرجع	IRR/USD	سیستم مالی	روزانه
27	قیمت گواهی کاهش انتشار کربن	IRR/ton CO₂	سیستم مالی	روزانه
۲-۳-۳. داده‌های عملیاتی و محدودیت‌ها
شماره	نام داده	توضیح
28	وضعیت تجهیزات (آنلاین/آفلاین/تعمیرات)	وضعیت عملیاتی هر تجهیز کلیدی
29	برنامه تعمیرات پیشگیرانه	زمان‌بندی تعمیرات برنامه‌ریزی‌شده
30	محدودیت‌های عملیاتی ایمنی	دما، فشار و دبی‌های حد مجاز
31	وضعیت کک‌زدگی کویل‌های ریفرمر	شاخص تخمینی مقاومت حرارتی
۲-۳-۴. داده‌های محیطی و پایداری
شماره	نام داده	واحد	منبع
32	انتشار CO₂ لحظه‌ای	ton/h	محاسبه‌شده از دبی سوخت
33	انتشار NOx	ppm	آنالایزر دودکش
34	مصرف ویژه انرژی (SEC) آمونیاک	GJ/ton	محاسبه‌شده
35	مصرف ویژه انرژی (SEC) اوره	GJ/ton	محاسبه‌شده
۲-۴. خروجی‌های سیستم (Outputs)
۲-۴-۱. خروجی‌های کنترلی (Action Space)
شماره	اقدام کنترلی	محدوده	واحد
1	نسبت بخار به کربن (S/C) ریفرمر	۲.۵ – ۴.۰	mol/mol
2	دمای خروجی ریفرمر اولیه (COT)	۷۵۰ – ۸۵۰	°C
3	دمای خروجی ریفرمر ثانویه	۹۵۰ – ۱۰۵۰	°C
4	فشار عملیاتی سنتز آمونیاک	۱۲۰ – ۲۵۰	bar
5	دبی هوای ورودی به ریفرمر ثانویه	۵۰ – ۱۰۰	% ظرفیت
6	دمای آب خنک‌کننده هدف	۲۵ – ۴۰	°C
7	دبی گردش آب خنک‌کننده	۵۰ – ۱۰۰	% ظرفیت
8	توان کمپرسورهای اصلی (سرعت)	۶۰ – ۱۰۰	%
9	نسبت بازیابی حرارت	۵۰ – ۹۰	%
10	دبی سوخت کمکی (در صورت نیاز)	۰ – ۱۰۰	% ظرفیت
11	تنظیمات شیرهای کنترلی کلیدی	۰ – ۱۰۰	% گشودگی
۲-۴-۲. خروجی‌های پیش‌بینی و گزارش‌دهی
شماره	خروجی	توضیح
12	پیش‌بینی مصرف انرژی ۲۴ ساعت آینده	بر اساس الگوهای تاریخی و شرایط پیش‌بینی‌شده
13	پیش‌بینی انتشار CO₂	بر اساس سناریوهای عملیاتی مختلف
14	شناسایی ناکارآمدی‌های انرژی	تشخیص نقاط اتلاف انرژی با دقت بالا
15	هشدارهای پیشگیرانه	هشدار در صورت انحراف از شرایط بهینه
16	داشبورد مدیریت انرژی	نمایش لحظه‌ای شاخص‌های کلیدی عملکرد انرژی
17	گزارش‌های دوره‌ای	گزارش‌های روزانه، هفتگی و ماهانه مصرف انرژی
18	توصیه‌های بهینه‌سازی	پیشنهادات عملی برای بهبود بهره‌وری انرژی
۲-۵. الزامات غیرعملیاتی
۲-۵-۱. الزامات عملکردی
تأخیر پاسخ کنترلی کمتر از ۵۰۰ میلی‌ثانیه

دقت پیش‌بینی مصرف انرژی با خطای کمتر از ۵٪

ضریب اطمینان خروجی‌ها ≥ ۹۵٪

قابلیت اجرا بر روی سرورهای صنعتی با در دسترس بودن ۹۹.۹۹٪

۲-۵-۲. الزامات امنیتی
احراز هویت چندمرحله‌ای برای دسترسی به سیستم

ثبت کامل لاگ‌های عملیاتی

رمزنگاری ارتباطات (TLS 1.3)

پشتیبان‌گیری خودکار با دوره ۶ ساعته

۲-۵-۳. الزامات یکپارچه‌سازی
سازگاری با پروتکل‌های صنعتی: OPC UA، Modbus TCP/IP، Profinet

قابلیت اتصال به DCS موجود

خروجی API برای اتصال به سیستم‌های سطح بالای سازمانی

۳. تولید داده‌های سنتتیک برای آموزش عامل یادگیری تقویتی
برای دستیابی به ضریب اطمینان بالا (≥۹۵%) و خطای پایین (≤۵%)، نیاز به حداقل ۱۰۰,۰۰۰ نمونه داده در بازه‌های زمانی مختلف داریم. کد زیر داده‌های سنتتیک با رویکرد فیزیک-آگاه (Physics-Informed) تولید می‌کند:

python
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import norm, truncnorm
import random

class KhorasanPetrochemicalDataGenerator:
    """
    داده‌ساز سنتتیک برای پتروشیمی خراسان
    مبتنی بر مدل‌های فیزیک-آگاه و محدودیت‌های ترمودینامیکی
    """
    
    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        
        # محدودیت‌های عملیاتی بر اساس اطلاعات واقعی
        self.limits = {
            'T_primary_reformer': (750, 850),      # °C
            'T_secondary_reformer': (950, 1050),    # °C
            'P_ammonia_reactor': (120, 250),        # bar
            'S_C_ratio': (2.5, 4.0),                # mol/mol
            'feed_gas_flow': (80000, 120000),       # Nm3/h
            'air_flow': (40000, 60000),             # Nm3/h
            'steam_flow': (120, 200),               # ton/h
            'compressor_power': (15, 35),           # MW
            'cooling_water_temp': (25, 40),         # °C
            'cooling_water_flow': (8000, 15000),    # m3/h
            'ambient_temp': (-5, 45),               # °C
            'ammonia_production': (30, 45),         # ton/h
            'urea_production': (45, 65),            # ton/h
            'melamine_production': (1.5, 3.0),      # ton/h
        }
        
        # متغیرهای غیرقابل کنترل (اختلالات)
        self.disturbances = {
            'feed_composition_CH4': (0.85, 0.95),
            'feed_composition_C2H6': (0.02, 0.08),
            'feed_composition_C3H8': (0.01, 0.04),
            'feed_composition_N2': (0.01, 0.03),
            'feed_composition_CO2': (0.005, 0.02),
            'coking_factor': (0.0, 0.3),  # ضریب کاهش راندمان بر اثر کک‌زدگی
        }
        
        # هزینه‌ها و قیمت‌ها (IRR)
        self.prices = {
            'gas_price': (5000, 8000),      # IRR per Nm3
            'electricity_price': (800, 1500), # IRR per kWh
            'ammonia_price': (18000, 25000),  # IRR per ton
            'urea_price': (12000, 18000),     # IRR per ton
            'melamine_price': (45000, 60000), # IRR per ton
            'carbon_credit_price': (500, 1500) # IRR per ton CO2
        }
        
    def _generate_time_series(self, n_samples, start_time=None):
        """تولید سری زمانی با نمونه‌برداری ۱ ثانیه‌ای"""
        if start_time is None:
            start_time = datetime.now() - timedelta(days=30)
        
        timestamps = [start_time + timedelta(seconds=i) for i in range(n_samples)]
        return timestamps
    
    def _add_noise(self, value, noise_std, min_val=None, max_val=None):
        """افزودن نویز گاوسی با محدودیت"""
        noisy = value + np.random.normal(0, noise_std * abs(value))
        if min_val is not None:
            noisy = max(noisy, min_val)
        if max_val is not None:
            noisy = min(noisy, max_val)
        return noisy
    
    def _simulate_reformer(self, feed_flow, S_C_ratio, T_primary, T_secondary, 
                           feed_composition, coking_factor):
        """
        شبیه‌سازی ریفرمر بر اساس موازنه جرم و انرژی
        بازگشت: دبی گاز سنتز، ترکیب، مصرف انرژی
        """
        # محاسبه دبی بخار
        steam_flow = feed_flow * S_C_ratio * 0.012  # تقریب تبدیل
        
        # اثر کک‌زدگی بر راندمان
        efficiency_factor = 1.0 - coking_factor * 0.3
        
        # بازده تبدیل متان بر اساس دما (مدل ساده آرنیوس)
        k_primary = 0.85 * (1 + 0.003 * (T_primary - 800)) * efficiency_factor
        k_secondary = 0.92 * (1 + 0.002 * (T_secondary - 1000)) * efficiency_factor
        
        # ترکیب گاز سنتز
        H2_fraction = 0.60 + 0.02 * (T_primary - 800)/50 + 0.01 * (1 - coking_factor)
        N2_fraction = 0.20 + 0.01 * (feed_composition['N2'] - 0.02)/0.01
        CH4_fraction = 0.15 - 0.02 * (T_primary - 800)/50 - 0.01 * k_primary
        Ar_fraction = 0.02 + 0.01 * (feed_composition['N2'] - 0.02)/0.01
        
        # نرمال‌سازی
        total = H2_fraction + N2_fraction + CH4_fraction + Ar_fraction
        H2_fraction /= total
        N2_fraction /= total
        CH4_fraction /= total
        Ar_fraction /= total
        
        # مصرف انرژی ریفرمر
        energy_consumption = feed_flow * 2.5 * (1 - 0.1 * coking_factor)  # GJ/h
        
        return {
            'syngas_flow': feed_flow * 1.8 * efficiency_factor,
            'H2_fraction': H2_fraction,
            'N2_fraction': N2_fraction,
            'CH4_fraction': CH4_fraction,
            'Ar_fraction': Ar_fraction,
            'steam_flow': steam_flow,
            'energy_consumption': energy_consumption,
            'efficiency': k_primary * k_secondary
        }
    
    def _simulate_ammonia_synthesis(self, syngas_flow, H2_fraction, N2_fraction, 
                                    P_reactor, T_reactor):
        """
        شبیه‌سازی سنتز آمونیاک با سینتیک واکنش
        بازگشت: دبی آمونیاک تولیدی، مصرف انرژی، تبدیل
        """
        # نسبت H2/N2 بهینه ۳ است
        H2_N2_ratio = H2_fraction / N2_fraction if N2_fraction > 0 else 3.0
        
        # ضریب تبدیل بر اساس دما و فشار (مدل ساده)
        conversion = 0.85 * (1 + 0.005 * (P_reactor - 180)/10) * \
                    (1 - 0.008 * (T_reactor - 450)/10)
        conversion = max(0.4, min(0.98, conversion))
        
        # تولید آمونیاک
        ammonia_flow = syngas_flow * 0.15 * conversion * (H2_N2_ratio / 3.0) * 0.8
        
        # مصرف انرژی کمپرسورها
        compressor_power = 20 * (P_reactor / 180) * (syngas_flow / 100000) * 0.9
        
        return {
            'ammonia_flow': max(20, min(55, ammonia_flow)),
            'conversion': conversion,
            'compressor_power': compressor_power,
            'H2_N2_ratio': H2_N2_ratio
        }
    
    def _simulate_urea_production(self, ammonia_flow, CO2_availability):
        """
        شبیه‌سازی تولید اوره از آمونیاک و CO2
        """
        # نسبت استوکیومتری ۲NH3 + CO2 → (NH2)2CO + H2O
        urea_flow = ammonia_flow * 0.75 * CO2_availability * 0.92
        return max(35, min(70, urea_flow))
    
    def _simulate_melamine_production(self, ammonia_flow, urea_flow):
        """
        شبیه‌سازی تولید ملامین از اوره
        """
        # مصرف اوره به عنوان خوراک ملامین
        urea_for_melamine = min(urea_flow * 0.15, 3.5)
        melamine_flow = urea_for_melamine * 0.28  # yield تقریبی
        return max(0.5, min(3.5, melamine_flow))
    
    def _calculate_emissions(self, feed_flow, energy_consumption, efficiency):
        """
        محاسبه انتشار CO2 بر اساس مصرف سوخت و بازده
        """
        # انتشار از احتراق سوخت
        combustion_CO2 = feed_flow * 0.002 * (1 - efficiency * 0.1)  # ton/h
        
        # انتشار فرآیندی
        process_CO2 = feed_flow * 0.0005  # ton/h
        
        return combustion_CO2 + process_CO2
    
    def generate_sample(self, t):
        """
        تولید یک نمونه داده کامل
        """
        # متغیرهای غیرقابل کنترل (اختلالات)
        feed_composition = {
            'CH4': np.random.uniform(*self.disturbances['feed_composition_CH4']),
            'C2H6': np.random.uniform(*self.disturbances['feed_composition_C2H6']),
            'C3H8': np.random.uniform(*self.disturbances['feed_composition_C3H8']),
            'N2': np.random.uniform(*self.disturbances['feed_composition_N2']),
            'CO2': np.random.uniform(*self.disturbances['feed_composition_CO2'])
        }
        
        # نرمال‌سازی ترکیب خوراک
        total = sum(feed_composition.values())
        for k in feed_composition:
            feed_composition[k] /= total
        
        coking_factor = np.random.uniform(*self.disturbances['coking_factor'])
        ambient_temp = np.random.uniform(*self.limits['ambient_temp'])
        
        # متغیرهای تصمیم (قابل کنترل توسط عامل)
        S_C_ratio = np.random.uniform(*self.limits['S_C_ratio'])
        T_primary = np.random.uniform(*self.limits['T_primary_reformer'])
        T_secondary = np.random.uniform(*self.limits['T_secondary_reformer'])
        P_reactor = np.random.uniform(*self.limits['P_ammonia_reactor'])
        T_reactor = 400 + 0.5 * (T_secondary - 950) + np.random.normal(0, 5)
        T_reactor = max(380, min(500, T_reactor))
        
        feed_flow = np.random.uniform(*self.limits['feed_gas_flow'])
        air_flow = np.random.uniform(*self.limits['air_flow'])
        
        cooling_water_temp = np.random.uniform(*self.limits['cooling_water_temp'])
        cooling_water_flow = np.random.uniform(*self.limits['cooling_water_flow'])
        
        # شبیه‌سازی ریفرمر
        reformer_result = self._simulate_reformer(
            feed_flow, S_C_ratio, T_primary, T_secondary,
            feed_composition, coking_factor
        )
        
        # شبیه‌سازی سنتز آمونیاک
        ammonia_result = self._simulate_ammonia_synthesis(
            reformer_result['syngas_flow'],
            reformer_result['H2_fraction'],
            reformer_result['N2_fraction'],
            P_reactor, T_reactor
        )
        
        ammonia_flow = ammonia_result['ammonia_flow']
        
        # شبیه‌سازی تولید اوره
        CO2_availability = 0.85 + 0.1 * (feed_composition['CO2'] / 0.02)
        urea_flow = self._simulate_urea_production(ammonia_flow, CO2_availability)
        
        # شبیه‌سازی تولید ملامین
        melamine_flow = self._simulate_melamine_production(ammonia_flow, urea_flow)
        
        # محاسبه انتشار
        total_emissions = self._calculate_emissions(
            feed_flow, 
            reformer_result['energy_consumption'],
            reformer_result['efficiency']
        )
        
        # محاسبه مصرف ویژه انرژی (SEC)
        SEC_ammonia = reformer_result['energy_consumption'] / ammonia_flow
        SEC_urea = (reformer_result['energy_consumption'] * 0.4) / urea_flow
        
        # قیمت‌ها (با تغییرات تصادفی روزانه)
        prices = {
            'gas': np.random.uniform(*self.prices['gas_price']),
            'electricity': np.random.uniform(*self.prices['electricity_price']),
            'ammonia': np.random.uniform(*self.prices['ammonia_price']),
            'urea': np.random.uniform(*self.prices['urea_price']),
            'melamine': np.random.uniform(*self.prices['melamine_price']),
            'carbon': np.random.uniform(*self.prices['carbon_credit_price'])
        }
        
        # محاسبه سودآوری
        revenue = (ammonia_flow * prices['ammonia'] + 
                   urea_flow * prices['urea'] + 
                   melamine_flow * prices['melamine'])
        
        energy_cost = (feed_flow * prices['gas'] * 0.001 + 
                      ammonia_result['compressor_power'] * 1000 * prices['electricity'] * 0.001)
        
        carbon_cost = total_emissions * prices['carbon']
        
        profit = revenue - energy_cost - carbon_cost
        
        # ساخت نمونه
        sample = {
            # ورودی‌ها (State)
            'timestamp': t,
            'feed_flow': feed_flow,
            'feed_CH4': feed_composition['CH4'],
            'feed_C2H6': feed_composition['C2H6'],
            'feed_C3H8': feed_composition['C3H8'],
            'feed_N2': feed_composition['N2'],
            'feed_CO2': feed_composition['CO2'],
            'coking_factor': coking_factor,
            'ambient_temp': ambient_temp,
            'S_C_ratio': S_C_ratio,
            'T_primary_reformer': T_primary,
            'T_secondary_reformer': T_secondary,
            'P_ammonia_reactor': P_reactor,
            'T_ammonia_reactor': T_reactor,
            'air_flow': air_flow,
            'cooling_water_temp': cooling_water_temp,
            'cooling_water_flow': cooling_water_flow,
            
            # خروجی‌ها (State/Observation)
            'syngas_flow': reformer_result['syngas_flow'],
            'H2_fraction': reformer_result['H2_fraction'],
            'N2_fraction': reformer_result['N2_fraction'],
            'CH4_fraction': reformer_result['CH4_fraction'],
            'Ar_fraction': reformer_result['Ar_fraction'],
            'steam_flow': reformer_result['steam_flow'],
            'reformer_efficiency': reformer_result['efficiency'],
            'reformer_energy': reformer_result['energy_consumption'],
            'ammonia_flow': ammonia_flow,
            'ammonia_conversion': ammonia_result['conversion'],
            'compressor_power': ammonia_result['compressor_power'],
            'H2_N2_ratio': ammonia_result['H2_N2_ratio'],
            'urea_flow': urea_flow,
            'melamine_flow': melamine_flow,
            'total_emissions': total_emissions,
            'SEC_ammonia': SEC_ammonia,
            'SEC_urea': SEC_urea,
            
            # پاداش (Reward)
            'profit': profit,
            'revenue': revenue,
            'energy_cost': energy_cost,
            'carbon_cost': carbon_cost,
            
            # قیمت‌ها
            'gas_price': prices['gas'],
            'electricity_price': prices['electricity'],
            'ammonia_price': prices['ammonia'],
            'urea_price': prices['urea'],
            'melamine_price': prices['melamine'],
            'carbon_price': prices['carbon']
        }
        
        # افزودن نویز به تمام مقادیر عددی
        for key in sample:
            if key != 'timestamp' and isinstance(sample[key], (int, float)):
                noise_level = 0.01  # 1% نویز
                sample[key] = self._add_noise(sample[key], noise_level)
        
        return sample
    
    def generate_dataset(self, n_samples=100000, save_path=None):
        """
        تولید مجموعه داده کامل
        """
        print(f"تولید {n_samples} نمونه داده...")
        
        start_time = datetime.now() - timedelta(days=30)
        timestamps = self._generate_time_series(n_samples, start_time)
        
        data = []
        for i, t in enumerate(timestamps):
            if i % 10000 == 0:
                print(f"پیشرفت: {i}/{n_samples} نمونه")
            sample = self.generate_sample(t)
            data.append(sample)
        
        df = pd.DataFrame(data)
        
        # محاسبه آمار توصیفی
        print("\nآمار توصیفی مجموعه داده:")
        print(df.describe())
        
        # ذخیره
        if save_path:
            df.to_csv(save_path, index=False)
            print(f"\nداده‌ها در {save_path} ذخیره شدند.")
        
        return df
    
    def validate_dataset(self, df):
        """
        اعتبارسنجی مجموعه داده بر اساس محدودیت‌های فیزیکی
        """
        print("\n=== اعتبارسنجی مجموعه داده ===")
        
        # بررسی محدودیت‌ها
        violations = 0
        for var, (min_val, max_val) in self.limits.items():
            if var in df.columns:
                outside = ((df[var] < min_val) | (df[var] > max_val)).sum()
                if outside > 0:
                    violations += outside
                    print(f"⚠ {var}: {outside} نمونه خارج از محدوده [{min_val}, {max_val}]")
        
        # بررسی همبستگی‌های فیزیکی
        correlations = {
            ('feed_flow', 'syngas_flow'): 0.6,
            ('T_primary_reformer', 'reformer_efficiency'): 0.4,
            ('S_C_ratio', 'steam_flow'): 0.7,
            ('P_ammonia_reactor', 'ammonia_conversion'): 0.3,
        }
        
        corr_violations = 0
        for (var1, var2), expected_corr in correlations.items():
            if var1 in df.columns and var2 in df.columns:
                actual_corr = df[var1].corr(df[var2])
                if abs(actual_corr - expected_corr) > 0.3:
                    corr_violations += 1
                    print(f"⚠ همبستگی {var1}-{var2}: انتظار {expected_corr:.2f}, "
                          f"دریافت {actual_corr:.2f}")
        
        if violations == 0 and corr_violations == 0:
            print("✅ مجموعه داده معتبر است.")
        else:
            print(f"⚠ {violations + corr_violations} مورد نقض محدودیت شناسایی شد.")
        
        return violations == 0 and corr_violations == 0


# اجرای تولید داده
if __name__ == "__main__":
    generator = KhorasanPetrochemicalDataGenerator(seed=42)
    
    # تولید 100,000 نمونه داده
    df = generator.generate_dataset(n_samples=100000, save_path="khorasan_petrochem_data.csv")
    
    # اعتبارسنجی
    generator.validate_dataset(df)
    
    # نمایش نمونه‌ای از داده‌ها
    print("\nنمونه داده تولید شده:")
    print(df.iloc[0].to_dict())
    
    # ذخیره در فرمت‌های مختلف برای استفاده در RL
    # داده‌های آموزشی (80%)
    train_df = df.sample(frac=0.8, random_state=42)
    test_df = df.drop(train_df.index)
    
    train_df.to_csv("khorasan_petrochem_train.csv", index=False)
    test_df.to_csv("khorasan_petrochem_test.csv", index=False)
    
    print(f"\n✅ داده‌های آموزشی: {len(train_df)} نمونه")
    print(f"✅ داده‌های آزمون: {len(test_df)} نمونه")
    print(f"✅ ضریب اطمینان تخمینی: 95.2%")
    print(f"✅ خطای پیش‌بینی تخمینی: 4.8%")
۳-۱. مشخصات داده‌های تولیدشده
پارامتر	مقدار
تعداد کل نمونه‌ها	۱۰۰,۰۰۰
داده‌های آموزشی	۸۰,۰۰۰ نمونه
داده‌های آزمون	۲۰,۰۰۰ نمونه
تعداد ویژگی‌ها	۴۲ ویژگی
بازه زمانی	۳۰ روز (نمونه‌برداری ۱ ثانیه‌ای)
ضریب اطمینان	≥ ۹۵.۲٪
خطای پیش‌بینی	≤ ۴.۸٪

> **توجه:** اعداد «ضریب اطمینان ۹۵.۲٪» و «خطای پیش‌بینی ۴.۸٪» در بالا بخشی از سند طراحی اولیه هستند و از پیش محاسبه نشده‌اند (در کد اصلی صرفاً چاپ می‌شدند، نه نتیجه اندازه‌گیری). در پیاده‌سازی واقعی این ریپو (بخش ۴ به بعد)، تمام متریک‌های عملکردی از بک‌تست واقعی محاسبه و گزارش می‌شوند؛ برای اعتبارسنجی صنعتی واقعی، کالیبراسیون با داده تاریخی SCADA لازم است.

---

## ۴. پیاده‌سازی نرم‌افزار (این ریپو)

این بخش، تبدیل سند الزامات بالا را به یک محصول نرم‌افزاری قابل اجرا مستند می‌کند: شبیه‌ساز فیزیک-آگاه، محیط یادگیری تقویتی، پایپ‌لاین آموزش/ارزیابی، و API سرویس‌دهی.

### ۴-۱. معماری

```
src/sems/
├── config.py         محدودیت‌ها/بازه‌ها/قیمت‌ها/فضای اقدام (از بخش‌های ۱ و ۲-۴-۱)
├── simulator.py       هسته فیزیکی مشترک (ریفرمر → سنتز آمونیاک → اوره → ملامین → انتشار → اقتصاد)
├── data_generator.py  تولید دیتاست سنتتیک (بخش ۳) با استفاده از simulator.py
├── env.py             KhorasanEnergyEnv - محیط Gymnasium (Box action ۱۱بعدی، Box observation)
├── train.py           آموزش عامل PPO (stable-baselines3)
├── evaluate.py         بک‌تست عامل در برابر baseline ثابت + محاسبه واقعی متریک‌ها
├── forecasting.py      پیش‌بینی افق ۲۴ساعته (Monte-Carlo rollout) + تشخیص ناکارآمدی/هشدار
└── api/                FastAPI: /health, /auth/token, /recommend, /forecast/*, /alerts, /report/{period}
scripts/generate_data.py   CLI تولید دیتاست train/test
tests/                      pytest برای simulator، env و API
```

**تصمیمات کلیدی:**
- هر گام محیط RL معادل یک بازه تصمیم **۱۵ دقیقه‌ای** است (نه نمونه‌برداری ۱ثانیه‌ای SCADA)؛ این فرکانس تصمیم کنترلی است، نه فرکانس پایش. هر اپیزود = یک روز عملیاتی (۹۶ گام).
- از ۱۱ اقدام کنترلی بخش ۲-۴-۱، هشت مورد مستقیماً در فیزیک شبیه‌ساز مدل شده‌اند؛ سه مورد (نسبت بازیابی حرارت، دبی سوخت کمکی، شیرهای کنترلی) با ضرایب ساده‌شده و مستند (کامنت `APPROX` در `simulator.py`) به مدل متصل شده‌اند.
- پاداش عامل = سود (درآمد − هزینه انرژی − هزینه کربن) منهای جریمه نقض محدودیت، مقیاس‌شده برای پایداری عددی آموزش.

### ۴-۲. نصب و اجرا

```bash
pip install -r requirements.txt
pip install -e .

# ۱. تولید دیتاست سنتتیک
python scripts/generate_data.py --n-samples 20000

# ۲. آموزش عامل RL
python -m sems.train --timesteps 50000 --model-path models/ppo_khorasan.zip

# ۳. ارزیابی در برابر baseline
python -m sems.evaluate --model-path models/ppo_khorasan.zip --episodes 20

# ۴. اجرای API
uvicorn sems.api.main:app --reload --port 8000
# سپس: POST /auth/token (کاربر دمو: operator / changeme) → Bearer token
```

اجرای تست‌ها:

```bash
pytest tests/
```

### ۴-۳. ماتریس ردیابی الزامات SRS

| الزام SRS | وضعیت | توضیح |
|---|---|---|
| مدل فیزیک-آگاه و تولید داده سنتتیک (بخش ۳) | ✅ پیاده‌سازی شد | `simulator.py`, `data_generator.py` |
| محیط RL با فضای حالت/اقدام (بخش ۲-۳, ۲-۴-۱) | ✅ پیاده‌سازی شد | `env.py` (Gymnasium) |
| آموزش عامل بهینه‌ساز | ✅ پیاده‌سازی شد | `train.py` (PPO/stable-baselines3) |
| توصیه کنترلی لحظه‌ای | ✅ پیاده‌سازی شد | `POST /recommend` |
| پیش‌بینی ۲۴ساعته مصرف/انتشار (بخش ۲-۴-۲) | ✅ پیاده‌سازی شد (rollout شبیه‌سازی) | `GET /forecast/energy`, `/forecast/emissions` |
| تشخیص ناکارآمدی و هشدار پیشگیرانه | ✅ پیاده‌سازی شد (قانون‌محور بر اساس SEC هدف) | `forecasting.detect_inefficiency`, `POST /alerts` |
| گزارش‌های دوره‌ای | ✅ پیاده‌سازی شد | `GET /report/{daily,weekly,monthly}` |
| احراز هویت چندمرحله‌ای (بخش ۲-۵-۲) | ⚠️ جایگزین نمایشی | JWT تک‌عاملی دمو، **نه** MFA سازمانی واقعی |
| رمزنگاری TLS 1.3 | ❌ خارج از دامنه ریپو | باید در لایه استقرار (reverse proxy/ingress) تأمین شود |
| اتصال واقعی SCADA/OPC UA/Modbus/Profinet/DCS | ❌ خارج از دامنه ریپو | نیازمند سخت‌افزار/زیرساخت صنعتی واقعی |
| در دسترس‌بودن ۹۹.۹۹٪ صنعتی | ❌ خارج از دامنه ریپو | مسئولیت لایه استقرار/زیرساخت است، نه کد اپلیکیشن |
| داشبورد مدیریت انرژی (وب) | ❌ خارج از دامنه این تحویل | API آماده است؛ می‌تواند در تحویل بعدی مصرف شود |

### ۴-۴. محدودیت شناخته‌شده: عدم تطابق مقیاس واحد SEC

اسموک‌تست این پیاده‌سازی نشان داد که فرمول ساده‌شده `energy_consumption` در `simulator.py` (به ارث‌رسیده از اسکریپت اصلی سند SRS، بدون تغییر منطق) مقادیر SEC را حدود ۷۰ برابر بزرگ‌تر از اهداف بخش ۱-۲ (۶۲.۶۱ GJ/ton آمونیاک، ۴.۵۲ GJ/ton اوره) تولید می‌کند. نتیجه عملی: `POST /alerts` و `POST /recommend` تقریباً همیشه هشدار «شدت بالا» برمی‌گردانند، صرف‌نظر از شرایط ورودی — این رفتار درست است نسبت به کد فعلی، اما بی‌فایده برای تصمیم‌گیری واقعی است. این ناهماهنگی در سند/اسکریپت اصلی از قبل وجود داشت (رجوع کنید به یادداشت بخش ۳-۱)؛ پیش از استفاده عملیاتی از `forecasting.detect_inefficiency`، باید فرمول انرژی ریفرمر با داده واقعی کارخانه کالیبره شود یا اهداف SEC بازتعریف شوند.

