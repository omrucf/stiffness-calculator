 private void StiffnessCalc1vw()
    {
      this.resultBean.H = this.paramBean.Pmhd1 / 2.0;
      this.resultBean.Sv = 2.0 * this.resultBean.H;
      this.resultBean.J = Math.Pow(this.resultBean.Sv, 3.0) / 12.0;
      this.resultBean.Sn = 1000.0 * this.resultBean.J * this.paramBean.JyxTxml / Math.Pow(this.paramBean.Gdzj, 3.0);
      this.resultBean.V1 = this.paramBean.Gdzj * Math.PI * 20.0 * 150.0;
      this.resultBean.V2 = this.paramBean.Gdzj * Math.PI * 20.0 * 150.0;
      this.resultBean.V3 = (Math.Pow(this.paramBean.Gdzj / 2.0 + this.paramBean.Pmhd1, 2.0) - Math.Pow(this.paramBean.Gdzj / 2.0, 2.0)) * Math.PI * 6000.0;
      this.resultBean.W1 = this.resultBean.V1 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W2 = this.resultBean.V2 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W3 = this.resultBean.V3 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W = this.resultBean.W1 + this.resultBean.W2 + this.resultBean.W3;
      this.resultBean.W0 = this.resultBean.W - this.resultBean.W2 / 2.0;
      this.txtSn.Text = string.Format("{0:F}", (object) this.resultBean.Sn);
      this.txtW1.Text = string.Format("{0:F}", (object) this.resultBean.W1);
      this.txtW2.Text = string.Format("{0:F}", (object) this.resultBean.W2);
      this.txtW3.Text = string.Format("{0:F}", (object) this.resultBean.W3);
      this.txtW.Text = string.Format("{0:F}", (object) this.resultBean.W);
      this.txtW0.Text = string.Format("{0:F}", (object) this.resultBean.W0);
    }

    private void StiffnessCalc1pr()
    {
      this.resultBean.Y1 = this.paramBean.Pmhd1 / 2.0; 
      this.resultBean.Y2 = this.paramBean.Pmhd1 + this.paramBean.BfmHd1 + this.paramBean.PpZjP / 2.0;
      this.resultBean.A1 = this.paramBean.Pmhd1 * this.paramBean.Pmkd1;
      this.resultBean.A2 = Math.Pow(this.paramBean.PpZjP / 2.0 + this.paramBean.BfmHd1, 2.0) * Math.PI - Math.Pow(this.paramBean.PpZjP / 2.0, 2.0) * Math.PI;
      this.resultBean.H = (this.resultBean.Y1 * this.resultBean.A1 + this.resultBean.Y2 * this.resultBean.A2) / (this.resultBean.A1 + this.resultBean.A2);
      this.resultBean.Y11 = Math.Abs(this.resultBean.H - this.resultBean.Y1);
      this.resultBean.Y21 = Math.Abs(this.resultBean.Y2 - this.resultBean.H);
      this.resultBean.J1 = this.paramBean.Pmkd1 * Math.Pow(this.paramBean.Pmhd1, 3.0) / 12.0;
      this.resultBean.J2 = Math.PI * (Math.Pow(this.paramBean.PpZjP + 2.0 * this.paramBean.BfmHd1, 4.0) - Math.Pow(this.paramBean.PpZjP, 4.0)) / 64.0;
      this.resultBean.J = (this.resultBean.J1 + this.resultBean.A1 * Math.Pow(this.resultBean.Y11, 2.0) + this.resultBean.J2 + this.resultBean.A2 * Math.Pow(this.resultBean.Y21, 2.0)) / this.paramBean.Pmkd1;
      this.resultBean.Sn = 1000.0 * this.resultBean.J * this.paramBean.JyxTxml / Math.Pow(this.paramBean.Gdzj, 3.0);
      this.resultBean.V1 = this.paramBean.Gdzj * Math.PI * 20.0 * 150.0;
      this.resultBean.V2 = this.paramBean.Gdzj * Math.PI * 20.0 * 150.0;
      this.resultBean.V3 = (Math.Pow(this.paramBean.Gdzj / 2.0 + this.paramBean.Pmhd1, 2.0) - Math.Pow(this.paramBean.Gdzj / 2.0, 2.0)) * Math.PI * 6000.0;
      this.resultBean.Sbf = Math.Pow(this.paramBean.PpZj / 2.0 + this.paramBean.BfmHd1, 2.0) * Math.PI - Math.Pow(this.paramBean.PpZj / 2.0, 2.0) * Math.PI;
      this.resultBean.Lpp = 6000.0 / this.paramBean.Pmkd1 * (this.paramBean.Gdzj + this.paramBean.Pmhd1 * 2.0) * Math.PI;
      this.resultBean.V4 = this.resultBean.Sbf * this.resultBean.Lpp;
      this.resultBean.W1 = this.resultBean.V1 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W2 = this.resultBean.V2 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W3 = this.resultBean.V3 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W4 = this.resultBean.V4 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W = this.resultBean.W1 + this.resultBean.W2 + this.resultBean.W3 + this.resultBean.W4;
      this.ppWeightAction = new PpWeightAction();
      this.resultBean.Wk = Convert.ToDouble(this.ppWeightAction.GetPpWeightWk(this.paramBean.PpZj));
      this.resultBean.Wp = this.resultBean.Lpp * this.resultBean.Wk / 1000.0;
      this.resultBean.Wz = this.resultBean.W1 + this.resultBean.W2 + this.resultBean.W3 + this.resultBean.W4 + this.resultBean.Wp;
      this.resultBean.W0 = this.resultBean.Wz - this.resultBean.W2 / 2.0;
      this.txtSn.Text = string.Format("{0:F}", (object) this.resultBean.Sn);
      this.txtW1.Text = string.Format("{0:F}", (object) this.resultBean.W1);
      this.txtW2.Text = string.Format("{0:F}", (object) this.resultBean.W2);
      this.txtW3.Text = string.Format("{0:F}", (object) this.resultBean.W3);
      this.txtW4.Text = string.Format("{0:F}", (object) this.resultBean.W4);
      this.txtWp.Text = string.Format("{0:F}", (object) this.resultBean.Wp);
      this.txtWz.Text = string.Format("{0:F}", (object) this.resultBean.Wz);
      this.txtW.Text = string.Format("{0:F}", (object) this.resultBean.W);
      this.txtW0.Text = string.Format("{0:F}", (object) this.resultBean.W0);
    }

    private void StiffnessCalc1op()
    {
      this.resultBean.Y1 = this.paramBean.Pmhd1 / 2.0;
      this.resultBean.Y2 = this.paramBean.Pmhd1 + this.paramBean.BfmHd1 + this.paramBean.PpZjP / 2.0;
      this.resultBean.Y3 = this.paramBean.Pmhd1 + 2.0 * this.paramBean.BfmHd1 + this.paramBean.PpZjP + this.paramBean.Pmhd2 / 2.0;
      this.resultBean.Y4 = this.paramBean.Pmhd1 + 2.0 * this.paramBean.BfmHd1 + this.paramBean.PpZjP + this.paramBean.Pmhd2 + this.paramBean.BfmHd2 + this.paramBean.PpZjP / 2.0;
      this.resultBean.A1 = this.paramBean.Pmhd1 * this.paramBean.Pmkd1;
      this.resultBean.A2 = Math.Pow(this.paramBean.PpZjP / 2.0 + this.paramBean.BfmHd1, 2.0) * Math.PI - Math.Pow(this.paramBean.PpZjP / 2.0, 2.0) * Math.PI;
      this.resultBean.A3 = this.paramBean.Pmhd2 * this.paramBean.Pmkd1;
      this.resultBean.A4 = Math.Pow(this.paramBean.PpZjP / 2.0 + this.paramBean.BfmHd2, 2.0) * Math.PI - Math.Pow(this.paramBean.PpZjP / 2.0, 2.0) * Math.PI;
      this.resultBean.H = (this.resultBean.Y1 * this.resultBean.A1 + this.resultBean.Y2 * this.resultBean.A2 + this.resultBean.Y3 * this.resultBean.A3 + this.resultBean.Y4 * this.resultBean.A4) / (this.resultBean.A1 + this.resultBean.A2 + this.resultBean.A3 + this.resultBean.A4);
      this.resultBean.Y11 = Math.Abs(this.resultBean.H - this.resultBean.Y1);
      this.resultBean.Y21 = Math.Abs(this.resultBean.Y2 - this.resultBean.H);
      this.resultBean.Y31 = Math.Abs(this.resultBean.Y3 - this.resultBean.H);
      this.resultBean.Y41 = Math.Abs(this.resultBean.Y4 - this.resultBean.H);
      this.resultBean.J1 = this.paramBean.Pmkd1 * Math.Pow(this.paramBean.Pmhd1, 3.0) / 12.0;
      this.resultBean.J2 = Math.PI / 64.0 * (Math.Pow(this.paramBean.PpZjP + 2.0 * this.paramBean.BfmHd1, 4.0) - Math.Pow(this.paramBean.PpZjP, 4.0));
      this.resultBean.J3 = this.paramBean.Pmkd1 * Math.Pow(this.paramBean.Pmhd2, 3.0) / 12.0;
      this.resultBean.J4 = Math.PI / 64.0 * (Math.Pow(this.paramBean.PpZjP + 2.0 * this.paramBean.BfmHd2, 4.0) - Math.Pow(this.paramBean.PpZjP, 4.0));
      this.resultBean.J = (this.resultBean.J1 + this.resultBean.A1 * Math.Pow(this.resultBean.Y11, 2.0) + this.resultBean.J2 + this.resultBean.A2 * Math.Pow(this.resultBean.Y21, 2.0) + this.resultBean.J3 + this.resultBean.A3 * Math.Pow(this.resultBean.Y31, 2.0) + this.resultBean.J4 + this.resultBean.A4 * Math.Pow(this.resultBean.Y41, 2.0)) / this.paramBean.Pmkd1;
      this.resultBean.Sn = 1000.0 * this.resultBean.J * this.paramBean.JyxTxml / Math.Pow(this.paramBean.Gdzj, 3.0);
      this.resultBean.V1 = this.paramBean.Gdzj * Math.PI * 20.0 * 150.0;
      this.resultBean.V2 = this.paramBean.Gdzj * Math.PI * 20.0 * 150.0;
      this.resultBean.V3 = (Math.Pow(this.paramBean.Gdzj / 2.0 + this.paramBean.Pmhd1, 2.0) - Math.Pow(this.paramBean.Gdzj / 2.0, 2.0)) * Math.PI * 6000.0;
      this.resultBean.Sbf = Math.Pow(this.paramBean.PpZj / 2.0 + this.paramBean.BfmHd1, 2.0) * Math.PI - Math.Pow(this.paramBean.PpZj / 2.0, 2.0) * Math.PI;
      this.resultBean.Lpp = 6000.0 / this.paramBean.Pmkd1 * (this.paramBean.Gdzj + this.paramBean.Pmhd1 * 2.0) * Math.PI;
      this.resultBean.V4 = this.resultBean.Sbf * this.resultBean.Lpp;
      this.resultBean.W1 = this.resultBean.V1 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W2 = this.resultBean.V2 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W3 = this.resultBean.V3 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W4 = this.resultBean.V4 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W = this.resultBean.W1 + this.resultBean.W2 + this.resultBean.W3 + this.resultBean.W4;
      this.ppWeightAction = new PpWeightAction();
      this.resultBean.Wk = Convert.ToDouble(this.ppWeightAction.GetPpWeightWk(this.paramBean.PpZj));
      this.resultBean.Wp = this.resultBean.Lpp * this.resultBean.Wk / 1000.0;
      this.resultBean.Wz = this.resultBean.W1 + this.resultBean.W2 + this.resultBean.W3 + this.resultBean.W4 + this.resultBean.Wp;
      this.resultBean.V3op = (Math.Pow(this.paramBean.Gdzj / 2.0 + this.paramBean.Pmhd1 + this.paramBean.PpZj + this.paramBean.BfmHd1 + this.paramBean.Pmhd2, 2.0) - Math.Pow(this.paramBean.Gdzj / 2.0 + this.paramBean.Pmhd1 + this.paramBean.PpZj + this.paramBean.BfmHd1, 2.0)) * Math.PI * 6000.0;
      this.resultBean.Sbfop = Math.Pow(this.paramBean.PpZj / 2.0 + this.paramBean.BfmHd2, 2.0) * Math.PI - Math.Pow(this.paramBean.PpZj / 2.0, 2.0) * Math.PI;
      this.resultBean.Lppop = 6000.0 / this.paramBean.Pmkd1 * (this.paramBean.Gdzj + this.paramBean.Pmhd1 * 2.0 + 2.0 * this.paramBean.PpZj + 2.0 * this.paramBean.BfmHd1 + 2.0 * this.paramBean.Pmhd2) * Math.PI;
      this.resultBean.V4op = this.resultBean.Sbfop * this.resultBean.Lppop;
      this.resultBean.W5 = this.resultBean.V3op * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W6 = this.resultBean.V4op * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.Wpop = this.resultBean.Lppop * this.resultBean.Wk / 1000.0;
      this.resultBean.Wop = this.resultBean.W5 + this.resultBean.W6 + this.resultBean.Wpop;
      double num = this.resultBean.Wz + this.resultBean.Wop;
      this.resultBean.W0 = num - this.resultBean.W2 / 2.0;
      this.txtSn.Text = string.Format("{0:F}", (object) this.resultBean.Sn);
      this.txtW1.Text = string.Format("{0:F}", (object) this.resultBean.W1);
      this.txtW2.Text = string.Format("{0:F}", (object) this.resultBean.W2);
      this.txtW3.Text = string.Format("{0:F}", (object) this.resultBean.W3);
      this.txtW4.Text = string.Format("{0:F}", (object) this.resultBean.W4);
      this.txtW5.Text = string.Format("{0:F}", (object) this.resultBean.W5);
      this.txtW6.Text = string.Format("{0:F}", (object) this.resultBean.W6);
      this.txtW.Text = string.Format("{0:F}", (object) this.resultBean.W);
      this.txtWp.Text = string.Format("{0:F}", (object) (this.resultBean.Wp + this.resultBean.Wpop));
      this.txtWz.Text = string.Format("{0:F}", (object) num);
      this.txtW0.Text = string.Format("{0:F}", (object) this.resultBean.W0);
    }

    private void StiffnessCalc1sq()
    {
      this.resultBean.Y1 = this.paramBean.Pmhd1 / 2.0;
      this.resultBean.Y2 = this.paramBean.Pmhd1 + this.paramBean.BfmHd1 + this.paramBean.PpZjP / 2.0;
      this.resultBean.Y3 = this.paramBean.Pmhd1 + 2.0 * this.paramBean.BfmHd1 + this.paramBean.PpZjP + this.paramBean.Pmhd2 / 2.0;
      this.resultBean.A1 = this.paramBean.Pmhd1 * this.paramBean.Pmkd1;
      this.resultBean.A2 = Math.Pow(this.paramBean.PpZj / 2.0 + this.paramBean.BfmHd1, 2.0) * Math.PI - Math.Pow(this.paramBean.PpZj / 2.0, 2.0) * Math.PI;
      this.resultBean.A3 = this.paramBean.Pmhd2 * this.paramBean.Pmkd1;
      this.resultBean.H = (this.resultBean.Y1 * this.resultBean.A1 + this.resultBean.Y2 * this.resultBean.A2 + this.resultBean.Y3 * this.resultBean.A3) / (this.resultBean.A1 + this.resultBean.A2 + this.resultBean.A3);
      this.resultBean.Y11 = Math.Abs(this.resultBean.H - this.resultBean.Y1);
      this.resultBean.Y21 = Math.Abs(this.resultBean.Y2 - this.resultBean.H);
      this.resultBean.Y31 = Math.Abs(this.resultBean.Y3 - this.resultBean.H);
      this.resultBean.J1 = this.paramBean.Pmkd1 * Math.Pow(this.paramBean.Pmhd1, 3.0) / 12.0;
      this.resultBean.J2 = Math.PI / 64.0 * (Math.Pow(this.paramBean.PpZjP + 2.0 * this.paramBean.BfmHd1, 4.0) - Math.Pow(this.paramBean.PpZjP, 4.0));
      this.resultBean.J3 = this.paramBean.Pmkd1 * Math.Pow(this.paramBean.Pmhd2, 3.0) / 12.0;
      this.resultBean.J = (this.resultBean.J1 + this.resultBean.A1 * Math.Pow(this.resultBean.Y11, 2.0) + this.resultBean.J2 + this.resultBean.A2 * Math.Pow(this.resultBean.Y21, 2.0) + this.resultBean.J3 + this.resultBean.A3 * Math.Pow(this.resultBean.Y31, 2.0)) / this.paramBean.Pmkd1;
      this.resultBean.Sn = 1000.0 * this.resultBean.J * this.paramBean.JyxTxml / Math.Pow(this.paramBean.Gdzj, 3.0);
      this.resultBean.V1 = this.paramBean.Gdzj * Math.PI * 20.0 * 150.0;
      this.resultBean.V2 = this.paramBean.Gdzj * Math.PI * 20.0 * 150.0;
      this.resultBean.V3 = (Math.Pow(this.paramBean.Gdzj / 2.0 + this.paramBean.Pmhd1, 2.0) - Math.Pow(this.paramBean.Gdzj / 2.0, 2.0)) * Math.PI * 6000.0;
      this.resultBean.Sbf = Math.Pow(this.paramBean.PpZj / 2.0 + this.paramBean.BfmHd1, 2.0) * Math.PI - Math.Pow(this.paramBean.PpZj / 2.0, 2.0) * Math.PI;
      this.resultBean.Lpp = 6000.0 / this.paramBean.Pmkd1 * (this.paramBean.Gdzj + this.paramBean.Pmhd1 * 2.0) * Math.PI;
      this.resultBean.V4 = this.resultBean.Sbf * this.resultBean.Lpp;
      this.resultBean.W1 = this.resultBean.V1 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W2 = this.resultBean.V2 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W3 = this.resultBean.V3 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W4 = this.resultBean.V4 * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.W = this.resultBean.W1 + this.resultBean.W2 + this.resultBean.W3 + this.resultBean.W4;
      this.ppWeightAction = new PpWeightAction();
      this.resultBean.Wk = Convert.ToDouble(this.ppWeightAction.GetPpWeightWk(this.paramBean.PpZj));
      this.resultBean.Wp = this.resultBean.Lpp * this.resultBean.Wk / 1000.0;
      this.resultBean.Vsq = (Math.Pow(this.paramBean.Gdzj / 2.0 + this.paramBean.Pmhd1 + this.paramBean.PpZj + this.paramBean.BfmHd1 + this.paramBean.Pmhd2, 2.0) - Math.Pow(this.paramBean.Gdzj / 2.0 + this.paramBean.Pmhd1 + this.paramBean.PpZj + this.paramBean.BfmHd1, 2.0)) * Math.PI * 6000.0;
      this.resultBean.Wsq = this.resultBean.Vsq * this.paramBean.JyxZd / 1000000.0;
      this.resultBean.Wz = this.resultBean.W1 + this.resultBean.W2 + this.resultBean.W3 + this.resultBean.W4 + this.resultBean.Wp + this.resultBean.Wsq;
      this.resultBean.W0 = this.resultBean.Wz - this.resultBean.W2 / 2.0;
      this.txtSn.Text = string.Format("{0:F}", (object) this.resultBean.Sn);
      this.txtW1.Text = string.Format("{0:F}", (object) this.resultBean.W1);
      this.txtW2.Text = string.Format("{0:F}", (object) this.resultBean.W2);
      this.txtW3.Text = string.Format("{0:F}", (object) this.resultBean.W3);
      this.txtW4.Text = string.Format("{0:F}", (object) this.resultBean.W4);
      this.txtW7.Text = string.Format("{0:F}", (object) this.resultBean.Wsq);
      this.txtW.Text = string.Format("{0:F}", (object) this.resultBean.W);
      this.txtWp.Text = string.Format("{0:F}", (object) this.resultBean.Wp);
      this.txtWz.Text = string.Format("{0:F}", (object) this.resultBean.Wz);
      this.txtW0.Text = string.Format("{0:F}", (object) this.resultBean.W0);
    }
